# Generated by Django 4.1.5 on 2023-01-09 21:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cities", "0002_alter_city_telegram"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="birthday",
            field=models.DateField(blank=True, null=True, verbose_name="Дата рождения"),
        ),
        migrations.AddField(
            model_name="profile",
            name="city",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="cities.city",
                verbose_name="Город",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="instagram",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Instagram"
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="name",
            field=models.CharField(blank=True, max_length=255, verbose_name="Имя"),
        ),
        migrations.AddField(
            model_name="profile",
            name="surname",
            field=models.CharField(blank=True, max_length=255, verbose_name="Фамилия"),
        ),
        migrations.AddField(
            model_name="profile",
            name="telegram",
            field=models.CharField(blank=True, max_length=255, verbose_name="Telegram"),
        ),
        migrations.AddField(
            model_name="profile",
            name="whatsapp",
            field=models.IntegerField(blank=True, null=True, verbose_name="WhatsApp"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(
                default="default.jpg", upload_to="profile_pics", verbose_name="Фото"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Имя пользователя",
            ),
        ),
    ]
