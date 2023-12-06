from django.shortcuts import render, redirect
from django.views import View
from .forms import DetectForm
from django.conf import settings
from ultralytics import YOLO
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
MODEL = YOLO("best.pt")


class DetectView(View):
    form_class = DetectForm
    template_name = "upload.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, "upload.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            MODEL.predict(
                image.image.path,
                save=True,
                project=settings.MEDIA_ROOT,
                name=f"{image.image.name}_predicted",
                imgsz=[640, 640],
            )
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


class LoginView(View):
    form_class = AuthenticationForm
    template_name = "login_signup.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("detect")
        return render(request, self.template_name, {"form": form})


class SignupView(View):
    form_class = UserCreationForm
    template_name = "login_signup.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form, "signup": True})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("detect")
        return render(request, self.template_name, {"form": form, "signup": True})


def logout_view(request):
    logout(request)
    return redirect("detect")
