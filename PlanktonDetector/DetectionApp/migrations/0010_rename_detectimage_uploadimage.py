# Generated by Django 4.2.7 on 2023-12-13 01:08

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("DetectionApp", "0009_remove_predictedimage_owner"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="DetectImage",
            new_name="UploadImage",
        ),
    ]
