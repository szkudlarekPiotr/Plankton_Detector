from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views import View
from .forms import DetectForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import UploadImage, PredictedImage
from .utils import predict_image
from django.contrib.auth.mixins import LoginRequiredMixin
import json


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
            for f in files:
                image = UploadImage(
                    image=f,
                )
                image.owner = request.user
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
                        prediction_data={"data": "no results"},
                    )
                else:
                    predicted_image = PredictedImage.objects.create(
                        original_image=image,
                        image=image.predicted_image_url,
                        prediction_data=results_metrics,
                    )
                predictions.append(predicted_image)
            return render(
                request,
                "results.html",
                {
                    "img_saved": True,
                    "img_url": predictions,
                },
            )
        else:
            return render(request, "upload.html", {"form": form})


class ListHistory(LoginRequiredMixin, ListView):
    model = PredictedImage
    queryset = PredictedImage.objects.all()
    template_name = "history.html"
    paginate_by = 3

    def get_queryset(self) -> QuerySet[Any]:
        queryset = PredictedImage.objects.filter(
            original_image__owner=self.request.user
        ).order_by("-date_predicted")
        return queryset


class DetectionDetails(LoginRequiredMixin, DetailView):
    model = PredictedImage
    template_name = "detection_detail.html"
