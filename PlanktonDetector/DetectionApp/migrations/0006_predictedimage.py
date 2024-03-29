# Generated by Django 4.2.7 on 2023-12-12 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("DetectionApp", "0005_detectimage_date_predicted"),
    ]

    operations = [
        migrations.CreateModel(
            name="PredictedImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="plankton/%Y/%m/%d/None")),
                ("confidence", models.FloatField()),
                ("class_name", models.CharField(max_length=100)),
                (
                    "original_image",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="DetectionApp.detectimage",
                    ),
                ),
            ],
        ),
    ]
