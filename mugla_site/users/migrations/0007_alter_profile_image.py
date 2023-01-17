# Generated by Django 4.1.5 on 2023-01-12 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_remove_profile_cropping_profile_cropping_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(
                default="default.jpg", upload_to="profile_pics", verbose_name="Фото"
            ),
        ),
    ]