from django.db import models

# Create your models here.

class DetectImage(models.Model):
    image = models.ImageField(upload_to="plankton/%Y/%m/%d/")