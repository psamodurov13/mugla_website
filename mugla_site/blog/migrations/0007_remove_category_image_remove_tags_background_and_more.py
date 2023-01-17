# Generated by Django 4.1.5 on 2023-01-11 10:36

from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_rename_background_category_image_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="category", name="image",),
        migrations.RemoveField(model_name="tags", name="background",),
        migrations.AddField(
            model_name="category",
            name="photo",
            field=models.ImageField(
                blank=True, upload_to="photo/%Y/%m/%d/", verbose_name="Фото"
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="cropping",
            field=image_cropping.fields.ImageRatioField(
                "photo",
                "1950x687",
                adapt_rotation=False,
                allow_fullsize=False,
                free_crop=False,
                help_text=None,
                hide_image_field=False,
                size_warning=True,
                verbose_name="Обрезанное фото для фона",
            ),
        ),
        migrations.AddField(
            model_name="tags",
            name="cropping",
            field=image_cropping.fields.ImageRatioField(
                "photo",
                "1950x687",
                adapt_rotation=False,
                allow_fullsize=False,
                free_crop=False,
                help_text=None,
                hide_image_field=False,
                size_warning=True,
                verbose_name="Обрезанное фото для фона",
            ),
        ),
        migrations.AddField(
            model_name="tags",
            name="photo",
            field=models.ImageField(
                blank=True, upload_to="photo/%Y/%m/%d/", verbose_name="Фото"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="cropping",
            field=image_cropping.fields.ImageRatioField(
                "photo",
                "1950x687",
                adapt_rotation=False,
                allow_fullsize=False,
                free_crop=False,
                help_text=None,
                hide_image_field=False,
                size_warning=True,
                verbose_name="Обрезанное фото для фона",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(max_length=255, unique=True, verbose_name="URL"),
        ),
        migrations.AlterField(
            model_name="post",
            name="photo",
            field=models.ImageField(
                blank=True, upload_to="photo/%Y/%m/%d/", verbose_name="Фото"
            ),
        ),
        migrations.AlterField(
            model_name="tags",
            name="slug",
            field=models.SlugField(max_length=255, unique=True, verbose_name="URL"),
        ),
    ]