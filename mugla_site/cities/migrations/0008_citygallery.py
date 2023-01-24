# Generated by Django 4.1.5 on 2023-01-23 23:49

from django.db import migrations, models
import django.db.models.deletion
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ("cities", "0007_alter_city_cropping_content_photo"),
    ]

    operations = [
        migrations.CreateModel(
            name="CityGallery",
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
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        upload_to="company_gallery/%Y/%m/%d/",
                        verbose_name="Доп. фото",
                    ),
                ),
                (
                    "cropping_gallery",
                    image_cropping.fields.ImageRatioField(
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
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="cities.city",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]