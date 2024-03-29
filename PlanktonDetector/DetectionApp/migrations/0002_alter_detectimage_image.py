# Generated by Django 4.2.7 on 2023-11-28 16:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("DetectionApp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="detectimage",
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
