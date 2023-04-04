from django.db import models
from cities.models import City

status = ['в процессе', 'завершен', 'не завершен']


class CollectData(models.Model):
    query = models.CharField(max_length=255, verbose_name='Запрос')
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='collect_data', verbose_name='Город')
    url = models.URLField(max_length=1000, blank=True, verbose_name='Ссылка на Google maps')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата сбора')
    collect_status = models.CharField(max_length=100, verbose_name='Статус')

    def __str__(self):
        return self.query

    class Meta:
        verbose_name = 'Сбор данных'
        verbose_name_plural = 'Сбор данных'
        ordering = ['-date']


