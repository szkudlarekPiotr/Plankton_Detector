# Generated by Django 4.2.7 on 2024-01-07 00:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Community", "0004_alter_post_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="date_added",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="date_pub",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
