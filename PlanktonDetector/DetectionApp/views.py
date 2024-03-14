from io import BytesIO, StringIO
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
import json
from django.shortcuts import render
from django.views import View
from .forms import DetectForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import PredictionBatch, UploadImage, PredictedImage
from .utils import predict_image
from django.contrib.auth.mixins import LoginRequiredMixin
import zipfile
from os.path import basename


class DetectView(View):
    form_class = DetectForm
    template_name = "upload.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, "upload.html", {"form": form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        files = request.FILES.getlist("image")
        predictions = []
        if form.is_valid():
            pred_batch = PredictionBatch.objects.create(owner=request.user)
            for f in files:
                image = UploadImage(
                    image=f,
                )
                image.save()
                prediction_results = predict_image(image)
                image.predicted_image_url = f"{image.image.name.split('.')[0]}_predicted.{image.image.name.split('.')[-1]}"
                image.save()
                if prediction_results["predictions"]:
                    predicted_image = PredictedImage.objects.create(
                        original_image=image,
                        image=image.predicted_image_url,
                        prediction_data=prediction_results,
                    )
                else:
                    predicted_image = PredictedImage.objects.create(
                        original_image=image,
                        image=image.image,
                        prediction_data={
                            "predictions": [{"confidence": "no predictions"}]
                        },
                    )
                predictions.append(predicted_image)
            pred_batch.images.add(*predictions)
            pred_batch.save()
            return render(
                request,
                "results.html",
                {
                    "img_saved": True,
                    "img": pred_batch,
                },
            )
        else:
            return render(request, "upload.html", {"form": form})


class ListHistory(LoginRequiredMixin, ListView):
    model = PredictionBatch
    queryset = PredictionBatch.objects.all()
    template_name = "history.html"
    paginate_by = 3

    def get_queryset(self) -> QuerySet[Any]:
        queryset = PredictionBatch.objects.filter(owner=self.request.user).order_by(
            "-date_predicted"
        )
        return queryset


class DetectionDetails(LoginRequiredMixin, DetailView):
    model = PredictionBatch
    template_name = "results.html"
    context_object_name = "img"


def download_pred(request, pk):
    zip = request.GET.get("zip", None)
    pred_batch = PredictionBatch.objects.get(pk=pk)
    if zip is None:
        txt = ""
        response = HttpResponse(content_type="text/plain")
        response["Content-Disposition"] = "attachment; filename=predictions.txt"
        for img in pred_batch.images.all():
            txt += f"Image {img.image.name.split('/')[-1]}\n"
            for prediction in img.get_prediction_data:
                txt += f"{prediction}\n"
        response.write(txt)
    elif zip == "True":
        archive = BytesIO()
        json = StringIO()
        with zipfile.ZipFile(archive, "w") as zip:
            for img in pred_batch.images.all():
                zip.write(img.image.path, basename(img.image.path))
                for prediction in img.get_prediction_data:
                    json.write(
                        f"Image {img.image.name.split('/')[-1]}: \n{prediction}\n"
                    )
            zip.writestr("predicitons.txt", json.getvalue())
        response = HttpResponse(archive.getvalue(), content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=predictions.zip"
        archive.seek(0)
    else:
        return HttpResponse(
            status=500, content=f"bad request - zip does not take argument {zip}"
        )
    return response
