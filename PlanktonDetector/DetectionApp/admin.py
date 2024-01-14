from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.UploadImage)
admin.site.register(models.PredictedImage)
admin.site.register(models.PredictionBatch)
