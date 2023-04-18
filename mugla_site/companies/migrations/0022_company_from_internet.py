# Generated by Django 4.1.5 on 2023-02-22 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0021_company_location"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="from_internet",
            field=models.BooleanField(
                default=False,
                verbose_name="Добавлено из интернета (загружено и автоматически переведено)",
            ),
        ),
    ]
