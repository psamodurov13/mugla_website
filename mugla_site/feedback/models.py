from django.db import models

from mugla_site.utils import CustomStr

# Create your models here.


class FeedbackCategory(CustomStr, models.Model):
    title = models.CharField(max_length=50, verbose_name='Категория сообщений')
    active = models.BooleanField(default=True, verbose_name='Включена')


class FeedbackMessage(CustomStr, models.Model):
    title = models.CharField(max_length=255, verbose_name='Тема сообщения')
    category = models.ForeignKey(FeedbackCategory, on_delete=models.PROTECT, related_name='category',
                                 verbose_name='Категория')
    email = models.EmailField(verbose_name='e-mail')
    text = models.TextField(verbose_name='Текст сообщения')
    processed = models.BooleanField(default=False, verbose_name='Обработано')

