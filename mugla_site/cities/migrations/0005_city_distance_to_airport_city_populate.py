# Generated by Django 4.1.5 on 2023-01-23 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cities", "0004_city_cropping_alter_city_photo_alter_city_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="city",
            name="distance_to_airport",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Расстояние до аэропорта"
            ),
        ),
        migrations.AddField(
            model_name="city",
            name="populate",
            field=models.IntegerField(blank=True, null=True, verbose_name="Население"),
        ),
    ]
