# Generated by Django 4.1.5 on 2023-03-28 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0022_company_from_internet"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="address",
            field=models.CharField(blank=True, max_length=255, verbose_name="Адрес"),
        ),
        migrations.AddField(
            model_name="company",
            name="open_hours",
            field=models.TextField(
                blank=True, max_length=1000, verbose_name="Часы работы"
            ),
        ),
    ]