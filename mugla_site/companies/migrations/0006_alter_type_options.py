# Generated by Django 4.1.5 on 2023-01-13 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0005_alter_type_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="type",
            options={
                "ordering": ["title"],
                "verbose_name": "Тип организации",
                "verbose_name_plural": "Типы",
            },
        ),
    ]
