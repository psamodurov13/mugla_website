from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

from cities.models import City
from phonenumber_field.modelfields import PhoneNumberField
from image_cropping import ImageCropField, ImageRatioField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Имя пользователя')
    slug = models.SlugField(max_length=255, verbose_name='URL')
    image = ImageCropField(upload_to='profile_pics', default='default.jpg', verbose_name='Исходное фото')
    cropping_avatar = ImageRatioField('image', '300x300', verbose_name='Обрезанное фото')
    name = models.CharField(max_length=255, blank=True, verbose_name='Имя')
    surname = models.CharField(max_length=255, blank=True, verbose_name='Фамилия')
    birthday = models.DateField(blank=True, verbose_name='Дата рождения', null=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='Город', null=True)
    whatsapp = PhoneNumberField(null=True, blank=True, verbose_name='WhatsApp')
    telegram = models.CharField(max_length=255, blank=True, verbose_name='Telegram')
    instagram = models.CharField(max_length=255, blank=True, verbose_name='Instagram')
    hidden = models.BooleanField(default=False, verbose_name='Скрыть контакты')

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        print('DICT - ', self.__dict__)
        return reverse('profile', kwargs={'slug': self.user.username})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

