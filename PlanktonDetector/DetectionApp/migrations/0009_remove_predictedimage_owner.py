# Generated by Django 4.2.7 on 2023-12-13 00:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("DetectionApp", "0008_predictedimage_owner"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="predictedimage",
            name="owner",
        ),
    ]