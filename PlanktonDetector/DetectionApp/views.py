from django.shortcuts import render
from .forms import DetectForm
from .models import DetectImage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


# Create your views here.


def view(request):
    form = DetectForm()
    if request.method == "GET":
        return render(request, "upload.html", {"form": form})
    form = DetectForm(request.POST, request.FILES)
    if form.is_valid():
        image = form.save()
        # detecting plankton
        saved = form.is_valid()
        return render(
            request, "upload.html", {"img_saved": saved, "img_path": image.image}
        )
    else:
        return render(request, "upload.html")
