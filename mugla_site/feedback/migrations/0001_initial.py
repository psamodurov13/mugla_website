# Generated by Django 4.1.5 on 2023-02-06 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FeedbackCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=50, verbose_name="Категория сообщений"),
                ),
                ("active", models.BooleanField(default=True, verbose_name="Включена")),
            ],
        ),
        migrations.CreateModel(
            name="FeedbackMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="Тема сообщения"),
                ),
                ("text", models.TextField(verbose_name="Текст сообщения")),
                (
                    "processed",
                    models.BooleanField(default=False, verbose_name="Обработано"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="category",
                        to="feedback.feedbackcategory",
                        verbose_name="Категория",
                    ),
                ),
            ],
        ),
    ]
