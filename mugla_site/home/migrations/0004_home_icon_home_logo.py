# Generated by Django 4.1.5 on 2023-02-21 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_home_content_photo_home_cropping_content_photo"),
    ]

    operations = [
        migrations.AddField(
            model_name="home",
            name="icon",
            field=models.ImageField(
                blank=True, upload_to="logos/", verbose_name="Фавиконка"
            ),
        ),
        migrations.AddField(
            model_name="home",
            name="logo",
            field=models.ImageField(
                blank=True, upload_to="logos/", verbose_name="Логотип"
            ),
        ),
    ]
