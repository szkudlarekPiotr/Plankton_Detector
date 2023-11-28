from django.shortcuts import render
from .forms import DetectForm
from .models import DetectImage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from ultralytics import YOLO

# Create your views here.
MODEL = YOLO("yolov8n.pt")


def view(request):
    if request.method == "GET":
        form = DetectForm()
        return render(request, "upload.html", {"form": form})
    form = DetectForm(request.POST, request.FILES)
    if form.is_valid():
        image = form.save()
        MODEL.predict(
            image.image.path,
            save=True,
            project=settings.MEDIA_ROOT,
            name=f"{image.image.name}_predicted",
            imgsz=[640, 640],
        )
        print(f"{settings.BASE_DIR}/predicted2/{image.image.name}")
        saved = form.is_valid()
        return render(
            request,
            "upload.html",
            {
                "img_saved": saved,
                "img_path": f"{image.image.name}_predicted/{image.image.name.split('/')[-1]}",
            },
        )
    else:
        return render(request, "upload.html", {"form": form})
