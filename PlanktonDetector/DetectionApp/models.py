import json
from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

# Create your models here.


class UploadImage(models.Model):
    image = models.ImageField(
        upload_to="plankton/%Y/%m/%d/",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png"])],
    )
    predicted_image_url = models.CharField(max_length=500)


class PredictedImage(models.Model):
    original_image = models.OneToOneField(UploadImage, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f"plankton/%Y/%m/%d/{original_image.name}")
    prediction_data = models.JSONField()

    @property
    def get_original_image(self):
        return self.original_image.image

    def get_prediction_data(self):
        results = json.loads(self.prediction_data)
        for pred in results:
            pred["confidence"] = round(pred["confidence"] * 100, 2)
        return results


class PredictionBatch(models.Model):
    images = models.ManyToManyField(PredictedImage)
    date_predicted = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
