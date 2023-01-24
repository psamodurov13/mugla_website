from django.db import models
from django.urls import reverse
from image_cropping import ImageRatioField

from mugla_site.utils import BaseModel, CustomGallery


class City(BaseModel, models.Model):
    title = models.CharField(max_length=50, verbose_name='Город')
    telegram = models.URLField(verbose_name='Telegram', blank=True)
    content = models.TextField(verbose_name='Контент')
    description = models.TextField(max_length=255, blank=True, verbose_name='Краткое описание')
    populate = models.IntegerField(verbose_name='Население', blank=True, null=True)
    distance_to_airport = models.IntegerField(verbose_name='Расстояние до аэропорта', blank=True, null=True)
    content_photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True, verbose_name='Фото в контенте')
    cropping_content_photo = ImageRatioField('content_photo', '400x300', size_warning=True,
                                             verbose_name='Обрезанное фото в контенте')

    def get_absolute_url(self):
        return reverse('city', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['title']


class CityGallery(CustomGallery):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='images')


def show_cities():
    cities = City.objects.all()
    return cities
