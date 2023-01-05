from django.db import models
from mugla_site.utils import CustomStr


class City(CustomStr, models.Model):
    title = models.CharField(max_length=50, verbose_name='Город')
    slug = models.SlugField(max_length=50, verbose_name='URL', unique=True)
    telegram = models.URLField(verbose_name='Telegram')
    content = models.TextField(verbose_name='Контент')
    description = models.TextField(max_length=255, blank=True, verbose_name='Краткое описание')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['title']
