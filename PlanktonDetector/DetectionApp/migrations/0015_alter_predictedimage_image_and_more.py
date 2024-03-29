# Generated by Django 4.2.7 on 2024-01-20 13:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("DetectionApp", "0014_alter_predictedimage_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="predictedimage",
            name="image",
            field=models.ImageField(
                upload_to="plankton/%Y/%m/%d/",
                validators=[django.core.validators.validate_image_file_extension],
            ),
        ),
        migrations.AlterField(
            model_name="predictionbatch",
            name="images",
            field=models.ManyToManyField(
                to="DetectionApp.predictedimage",
                validators=[django.core.validators.validate_image_file_extension],
            ),
        ),
        migrations.AlterField(
            model_name="uploadimage",
            name="image",
            field=models.ImageField(
                upload_to="plankton/%Y/%m/%d",
                validators=[django.core.validators.validate_image_file_extension],
            ),
        ),
    ]
