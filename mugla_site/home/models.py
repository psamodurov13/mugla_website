from django.db import models

# Create your models here.
from image_cropping import ImageRatioField

from mugla_site.utils import BaseModel


class Home(BaseModel):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    content = models.TextField()
    description = models.TextField(max_length=1000, blank=True)
    content_photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True, verbose_name='Фото в контенте')
    cropping_content_photo = ImageRatioField('content_photo', '400x300', size_warning=True,
                                             verbose_name='Обрезанное фото в контенте')
    logo = models.ImageField(upload_to='logos/', blank=True, verbose_name='Логотип')
    icon = models.ImageField(upload_to='logos/', blank=True, verbose_name='Фавиконка')

