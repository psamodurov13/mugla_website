# Generated by Django 4.1.5 on 2023-01-20 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0011_alter_profile_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="profile",
            options={"verbose_name": "Профиль", "verbose_name_plural": "Профили"},
        ),
    ]
