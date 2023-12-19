from django import forms
from pyparsing import removeQuotes
from .models import UploadImage
from django.forms import ClearableFileInput, HiddenInput
from django.contrib.auth.models import User


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class DetectForm(forms.Form):
    image = MultipleFileField()
    predicted_image_url = forms.CharField(
        max_length=500, widget=HiddenInput(), required=False
    )
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(), widget=HiddenInput(), required=False
    )
