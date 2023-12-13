from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.views import View

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
