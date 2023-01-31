from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from image_cropping import ImageRatioField
from phonenumber_field.modelfields import PhoneNumberField
from mptt.models import MPTTModel, TreeForeignKey

from mugla_site.utils import BaseModel, CustomGallery
from cities.models import City


class Type(BaseModel, MPTTModel):
    title = models.CharField(max_length=50, verbose_name='Тип организации')
    parent = TreeForeignKey('self', blank=True, null=True, on_delete=models.PROTECT, related_name='children')

    def get_absolute_url(self):
        return reverse('type', kwargs={'slug': self.slug})

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Тип организации'
        verbose_name_plural = 'Типы'
        ordering = ['title']


class CompanyTags(BaseModel):
    title = models.CharField(max_length=50, verbose_name='Тег')

    def get_absolute_url(self):
        return reverse('company-tags', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']


class Company(BaseModel, models.Model):
    title = models.CharField(max_length=255, verbose_name='Компания')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='companies', verbose_name='Автор')
    content = models.TextField(verbose_name='Контент')
    description = models.TextField(max_length=255, blank=True, verbose_name='Краткое описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    type = TreeForeignKey(Type, on_delete=models.PROTECT, related_name='companies', verbose_name='Тип организации')
    tags = models.ManyToManyField(CompanyTags, verbose_name='Теги', blank=True, related_name='companies')
    cities = models.ManyToManyField(City, verbose_name='Города', blank=True, related_name='companies')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    site = models.URLField(blank=True, verbose_name='Сайт')
    phone = PhoneNumberField(null=True, blank=True, verbose_name='Телефон')
    whatsapp = PhoneNumberField(null=True, blank=True, verbose_name='WhatsApp')
    telegram = models.CharField(max_length=255,  blank=True, verbose_name='Telegram')
    note = models.CharField(max_length=255,  blank=True, verbose_name='Полезная заметка')
    cropping_thumb = ImageRatioField('photo', '400x300', size_warning=True, verbose_name='Обрезанное фото для каталога')
    russian_speak = models.BooleanField(default=False, verbose_name='Есть русскоговорящий персонал')
    english_speak = models.BooleanField(default=False, verbose_name='Есть англоговорящий персонал')

    def get_absolute_url(self):
        return reverse('company', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['-created_at']


class CompanyGallery(CustomGallery):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='images')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')


class ChangeCompany(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='changes', verbose_name='Компания')
    title = models.CharField(max_length=255, verbose_name='Компания')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='changes', verbose_name='Автор')
    content = models.TextField(verbose_name='Контент')
    description = models.TextField(max_length=255, blank=True, verbose_name='Краткое описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    type = TreeForeignKey(Type, on_delete=models.PROTECT, related_name='changes', verbose_name='Тип организации')
    tags = models.ManyToManyField(CompanyTags, verbose_name='Теги', blank=True, related_name='changes')
    cities = models.ManyToManyField(City, verbose_name='Города', blank=True, related_name='changes')
    site = models.URLField(blank=True, verbose_name='Сайт')
    phone = PhoneNumberField(null=True, blank=True, verbose_name='Телефон')
    whatsapp = PhoneNumberField(null=True, blank=True, verbose_name='WhatsApp')
    telegram = models.CharField(max_length=255, blank=True, verbose_name='Telegram')
    note = models.CharField(max_length=255, blank=True, verbose_name='Полезная заметка')
    russian_speak = models.BooleanField(default=False, verbose_name='Есть русскоговорящий персонал')
    english_speak = models.BooleanField(default=False, verbose_name='Есть англоговорящий персонал')
    processed = models.BooleanField(default=False, verbose_name='Обработано')


def show_company_types():
    types = Type.objects.all()
    return types




