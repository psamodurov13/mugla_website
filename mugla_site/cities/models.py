from django.db import models
from django.urls import reverse

from mugla_site.utils import BaseModel


class City(BaseModel, models.Model):
    title = models.CharField(max_length=50, verbose_name='Город')
    telegram = models.URLField(verbose_name='Telegram', blank=True)
    content = models.TextField(verbose_name='Контент')
    description = models.TextField(max_length=255, blank=True, verbose_name='Краткое описание')

    def get_absolute_url(self):
        return reverse('city', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['title']


def show_cities():
    cities = City.objects.all()
    return cities
