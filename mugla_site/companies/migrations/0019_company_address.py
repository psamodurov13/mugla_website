# Generated by Django 4.1.5 on 2023-02-01 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0018_alter_changecompany_content_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="address",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
