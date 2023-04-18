# Generated by Django 4.1.5 on 2023-02-21 09:03

from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_alter_home_photo"),
    ]

    operations = [
        migrations.AddField(
            model_name="home",
            name="content_photo",
            field=models.ImageField(
                blank=True, upload_to="photo/%Y/%m/%d/", verbose_name="Фото в контенте"
            ),
        ),
        migrations.AddField(
            model_name="home",
            name="cropping_content_photo",
            field=image_cropping.fields.ImageRatioField(
                "content_photo",
                "400x300",
                adapt_rotation=False,
                allow_fullsize=False,
                free_crop=False,
                help_text=None,
                hide_image_field=False,
                size_warning=True,
                verbose_name="Обрезанное фото в контенте",
            ),
        ),
    ]