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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class PredictedImage(models.Model):
    original_image = models.OneToOneField(UploadImage, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f"plankton/%Y/%m/%d/{original_image.name}")
    confidence = models.FloatField()
    class_name = models.CharField(max_length=100)
    date_predicted = models.DateTimeField(auto_now_add=True)

    @property
    def get_owner(self):
        return self.original_image.owner

    @property
    def get_original_image(self):
        return self.original_image.image
