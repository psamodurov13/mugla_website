# Generated by Django 4.1.5 on 2023-01-17 21:08

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0009_companygallery_cropping_gallery"),
    ]

    operations = [
        migrations.AlterField(
            model_name="companygallery",
            name="cropping_gallery",
            field=image_cropping.fields.ImageRatioField(
                "image",
                "400x300",
                adapt_rotation=False,
                allow_fullsize=False,
                free_crop=False,
                help_text=None,
                hide_image_field=False,
                size_warning=True,
                verbose_name="Обрезанное доп фото",
            ),
        ),
    ]
