from django.db import models
from django.urls import reverse
from image_cropping import ImageRatioField
from django.contrib.gis.db import models as models_loc

from mugla_site.utils import BaseModel, CustomGallery


class Region(BaseModel):
    title = models.CharField(max_length=50, verbose_name='Название региона')
    content = models.TextField(verbose_name='Описание')
    location = models_loc.PointField(help_text="Use map widget for point the house location", blank=True, null=True)


class City(BaseModel, models.Model):
    title = models.CharField(max_length=50, verbose_name='Город')
    region = models.ForeignKey(Region, on_delete=models.PROTECT, verbose_name='Регион')
    telegram = models.URLField(verbose_name='Telegram', blank=True)
    content = models.TextField(verbose_name='Контент')
    description = models.TextField(max_length=255, blank=True, verbose_name='Краткое описание')
    populate = models.IntegerField(verbose_name='Население', blank=True, null=True)
    distance_to_airport = models.IntegerField(verbose_name='Расстояние до аэропорта', blank=True, null=True)
    content_photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True, verbose_name='Фото в контенте')
    cropping_content_photo = ImageRatioField('content_photo', '400x300', size_warning=True,
                                             verbose_name='Обрезанное фото в контенте')
    location = models_loc.PointField(help_text="Use map widget for point the house location", blank=True, null=True)

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
