# Generated by Django 4.2.13 on 2024-07-04 12:51

import digitalSociety.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("digitalSociety", "0002_citizens_picture_citizens_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="citizens",
            name="picture",
            field=models.ImageField(
                default="default.png",
                upload_to=digitalSociety.models.profile_picture_path,
            ),
        ),
    ]