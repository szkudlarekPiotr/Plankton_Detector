from django import forms
from .models import DetectImage

class DetectForm(forms.ModelForm):
    
    class Meta:
        model = DetectImage
        fields = "__all__"
        labels={"image":""}