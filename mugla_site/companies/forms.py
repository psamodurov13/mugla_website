from django import forms
from image_cropping import ImageCropWidget
from phonenumber_field.formfields import PhoneNumberField

from .models import *


class CreateCompanyForm(forms.ModelForm):
    phone = PhoneNumberField()
    whatsapp = PhoneNumberField()

    class Meta:
        model = Company

        fields = ['title', 'photo', 'content', 'description', 'type', 'tags', 'cities', 'site', 'phone', 'whatsapp', 'telegram',
                  'note', 'cropping_thumb', 'russian_speak', 'english_speak']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'cities': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'site': forms.URLInput(attrs={'class': 'form-control'}),
            'telegram': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control'}),
            'cropping_thumb': ImageCropWidget,
            'russian_speak': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'english_speak': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }



#         'author', 'created_at', 'views', 'is_published'
#
# title = models.CharField(max_length=255, verbose_name='Пост')
# author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='companies', verbose_name='Автор')
# content = models.TextField(verbose_name='Контент')
# description = models.TextField(max_length=255, blank=True, verbose_name='Краткое описание')
# created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
# views = models.IntegerField(default=0, verbose_name='Количество просмотров')
# type = TreeForeignKey(Type, on_delete=models.PROTECT, related_name='companies', verbose_name='Тип организации')
# tags = models.ManyToManyField(CompanyTags, verbose_name='Теги', blank=True, related_name='companies')
# cities = models.ManyToManyField(City, verbose_name='Города', blank=True, related_name='companies')
# is_published = models.BooleanField(default=False, verbose_name='Опубликован')
# site = models.URLField(blank=True, verbose_name='Сайт')
# phone = PhoneNumberField(null=True, blank=True, verbose_name='Телефон')
# whatsapp = PhoneNumberField(null=True, blank=True, verbose_name='WhatsApp')
# telegram = models.CharField(max_length=255,  blank=True, verbose_name='Telegram')
# note = models.CharField(max_length=255,  blank=True, verbose_name='Полезная заметка')
# cropping_thumb = ImageRatioField('photo', '400x300', size_warning=True, verbose_name='Обрезанное фото для каталога')
# russian_speak = models.BooleanField(default=False, verbose_name='Есть русскоговорящий персонал')
# english_speak = models.BooleanField(default=False, verbose_name='Есть англоговорящий персонал')
