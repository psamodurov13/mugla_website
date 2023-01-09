from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from mugla_site.utils import CustomStr
from cities.models import City


class Category(CustomStr, models.Model):
    title = models.CharField(max_length=50, verbose_name='Категория')
    slug = models.SlugField(max_length=50, verbose_name='URL', unique=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Tags(CustomStr, models.Model):
    title = models.CharField(max_length=50, verbose_name='Тег')
    slug = models.SlugField(max_length=50, verbose_name='URL', unique=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']


class Post(CustomStr, models.Model):
    title = models.CharField(max_length=255, verbose_name='Пост')
    slug = models.SlugField(max_length=255, verbose_name='URL', unique=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='posts', verbose_name='Автор')
    content = models.TextField(verbose_name='Контент')
    description = models.TextField(max_length=255, blank=True, verbose_name='Краткое описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField(Tags, verbose_name='Теги', blank=True, related_name='post')
    cities = models.ManyToManyField(City, verbose_name='Города', blank=True, related_name='post')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']


def show_categories():
    categories = Category.objects.all()
    return categories


def show_tags():
    tags = Tags.objects.all()
    return tags


