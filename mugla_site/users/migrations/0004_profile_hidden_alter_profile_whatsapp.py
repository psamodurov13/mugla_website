# Generated by Django 4.1.5 on 2023-01-10 15:14

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_profile_whatsapp"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="hidden",
            field=models.BooleanField(default=False, verbose_name="Скрыть контакты"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="whatsapp",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True,
                max_length=128,
                null=True,
                region=None,
                verbose_name="WhatsApp",
            ),
        ),
    ]
