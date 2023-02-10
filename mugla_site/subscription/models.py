from django.db import models


class Subscription(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    email = models.EmailField(unique=True, verbose_name='E-mail')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
