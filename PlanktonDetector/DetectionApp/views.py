from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .forms import DetectForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import PredictionBatch, UploadImage, PredictedImage
from .utils import predict_image
from django.contrib.auth.mixins import LoginRequiredMixin


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
                prediciton_results = predict_image(image)
                image.predicted_image_url = (
                    f"{image.image.name}_predicted/{image.image.name.split('/')[-1]}"
                )
                image.save()
                try:
                    results_metrics = prediciton_results
                except IndexError as e:
                    predicted_image = PredictedImage.objects.create(
                        original_image=image,
                        image=image.predicted_image_url,
                        prediction_data={"data": "no predicitions"},
                    )
                else:
                    predicted_image = PredictedImage.objects.create(
                        original_image=image,
                        image=image.predicted_image_url,
                        prediction_data=results_metrics,
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


def download_pred_res(request, pk):
    pred_batch = PredictionBatch.objects.get(pk=pk)
    response = HttpResponse(content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename=predictions.txt"
    for img in pred_batch.images.all():
        response.write(img.prediction_data)
    return response
