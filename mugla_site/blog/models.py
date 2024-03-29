from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from image_cropping import ImageRatioField
from mptt.models import MPTTModel, TreeForeignKey

from mugla_site.utils import BaseModel
from cities.models import City
from mugla_site.tasks import send_html_email_to_user
from mugla_site.settings import domain


class Category(BaseModel, MPTTModel):
    title = models.CharField(max_length=50, verbose_name='Категория')
    parent = TreeForeignKey('self', blank=True, null=True, on_delete=models.PROTECT, related_name='children')

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Tags(BaseModel, models.Model):
    title = models.CharField(max_length=50, verbose_name='Тег')

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']


class Post(BaseModel, models.Model):
    title = models.CharField(max_length=255, verbose_name='Пост')
    photo = models.ImageField(default='default_post.jpeg', upload_to='photo/%Y/%m/%d/', blank=True, verbose_name='Фото')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    content = models.TextField(verbose_name='Контент')
    description = models.TextField(max_length=255, blank=True, verbose_name='Краткое описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    category = TreeForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField(Tags, verbose_name='Теги', blank=True, related_name='post')
    cities = models.ManyToManyField(City, verbose_name='Города', blank=True, related_name='post')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    cropping_thumb = ImageRatioField('photo', '444x250', size_warning=True, verbose_name='Обрезанное фото для каталога')
    important = models.BooleanField(default=False, verbose_name='Важная статья')

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    # def save(self):
    #     if self.id:
    #         url = f'{domain}blog/posts/{self.slug}/'
    #         old_foo = Post.objects.get(pk=self.id)
    #         if old_foo.is_published == False and self.is_published == True:
    #             send_html_email_to_user.delay(
    #                 self.author.email,
    #                 'Ваша публикация прошла модерацию',
    #                 f'Публикация прошла модерацию и доступна по адресу <a href="{url}">{url}</a>'
    #             )
    #     super(Post, self).save()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']


def show_categories():
    categories = Category.objects.all()
    return categories




