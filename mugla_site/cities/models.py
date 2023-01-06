from django.db import models
from django.urls import reverse

from mugla_site.utils import CustomStr


class City(CustomStr, models.Model):
    title = models.CharField(max_length=50, verbose_name='Город')
    slug = models.SlugField(max_length=50, verbose_name='URL', unique=True)
    telegram = models.URLField(verbose_name='Telegram', blank=True)
    content = models.TextField(verbose_name='Контент')
    description = models.TextField(max_length=255, blank=True, verbose_name='Краткое описание')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')

    def get_absolute_url(self):
        return reverse('city', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['title']


def show_cities():
    cities = City.objects.all()
    return cities
