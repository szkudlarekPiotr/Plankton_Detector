# Generated by Django 4.2.7 on 2023-12-13 00:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("DetectionApp", "0006_predictedimage"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="detectimage",
            name="date_predicted",
        ),
        migrations.AddField(
            model_name="predictedimage",
            name="date_predicted",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
