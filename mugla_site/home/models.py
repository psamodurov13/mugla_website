from django.db import models

# Create your models here.
from mugla_site.utils import BaseModel


class Home(BaseModel):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    content = models.TextField()
    description = models.TextField(max_length=255, blank=True)
