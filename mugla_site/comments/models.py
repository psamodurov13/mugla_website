from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from blog.models import Post
from companies.models import Company


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comment', verbose_name='Автор')
    content = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    active = models.BooleanField(default=False, verbose_name='Опубликован')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']


class PostComments(Comments):
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='comment', verbose_name='Пост')


class CompanyComments(Comments):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='comment', verbose_name='Компания')


