from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from cities.models import City
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Имя пользователя')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', verbose_name='Фото')
    name = models.CharField(max_length=255, blank=True, verbose_name='Имя')
    surname = models.CharField(max_length=255, blank=True, verbose_name='Фамилия')
    birthday = models.DateField(blank=True, verbose_name='Дата рождения', null=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='Город', null=True)
    # whatsapp = models.IntegerField(blank=True, verbose_name='WhatsApp', null=True)
    whatsapp = PhoneNumberField(null=True, blank=True)
    telegram = models.CharField(max_length=255, blank=True, verbose_name='Telegram')
    instagram = models.CharField(max_length=255, blank=True, verbose_name='Instagram')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
