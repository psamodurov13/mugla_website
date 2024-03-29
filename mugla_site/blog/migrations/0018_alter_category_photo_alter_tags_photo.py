# Generated by Django 4.1.5 on 2023-01-31 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0017_alter_post_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="photo",
            field=models.ImageField(
                blank=True,
                default="default_post.jpeg",
                upload_to="photo/%Y/%m/%d/",
                verbose_name="Фото",
            ),
        ),
        migrations.AlterField(
            model_name="tags",
            name="photo",
            field=models.ImageField(
                blank=True,
                default="default_post.jpeg",
                upload_to="photo/%Y/%m/%d/",
                verbose_name="Фото",
            ),
        ),
    ]
