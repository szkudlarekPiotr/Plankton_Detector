from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.


class DetectImage(models.Model):
    image = models.ImageField(
        upload_to="plankton/%Y/%m/%d/",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png"])],
    )
