from django import forms
from .models import UploadImage


class DetectForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = [
            "image",
        ]
        labels = {"image": ""}
