# Generated by Django 4.1.5 on 2023-01-31 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cities", "0008_citygallery"),
    ]

    operations = [
        migrations.AlterField(
            model_name="city",
            name="photo",
            field=models.ImageField(
                blank=True,
                default="default_post.jpeg",
                upload_to="photo/%Y/%m/%d/",
                verbose_name="Фото",
            ),
        ),
    ]
