from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django.utils.safestring import mark_safe
from image_cropping import ImageCroppingMixin

from .models import *
from mugla_site.utils import BaseAdmin

from blog.models import City
from mugla_site.utils import CKEditorForm


# Register your models here.
class CityAdminForm(CKEditorForm, forms.ModelForm):

    class Meta:
        model = City
        fields = '__all__'


class CityAdmin(ImageCroppingMixin, BaseAdmin):
    form = CityAdminForm
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    fields = ('title', 'slug', 'content', 'description', 'photo', 'cropping', 'get_photo', 'telegram')


admin.site.register(City, CityAdmin)

admin.site.site_title = 'Управление сайтом'
admin.site.site_header = 'Управление сайтом'

