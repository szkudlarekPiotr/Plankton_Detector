# Generated by Django 4.2.7 on 2024-01-20 14:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("DetectionApp", "0015_alter_predictedimage_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="predictedimage",
            name="image",
            field=models.ImageField(upload_to="plankton/%Y/%m/%d/"),
        ),
        migrations.AlterField(
            model_name="predictionbatch",
            name="images",
            field=models.ManyToManyField(to="DetectionApp.predictedimage"),
        ),
        migrations.AlterField(
            model_name="uploadimage",
            name="image",
            field=models.ImageField(
                upload_to="plankton/%Y/%m/%d/",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpg", "png"]
                    )
                ],
            ),
        ),
    ]
