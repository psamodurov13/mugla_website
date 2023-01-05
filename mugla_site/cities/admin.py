from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django.utils.safestring import mark_safe
from .models import *
from mugla_site.utils import BaseAdmin

from blog.models import City
from mugla_site.utils import CKEditorForm


# Register your models here.
class CityAdminForm(CKEditorForm, forms.ModelForm):

    class Meta:
        model = City
        fields = '__all__'


class CityAdmin(BaseAdmin, admin.ModelAdmin):
    form = CityAdminForm
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    fields = ('title', 'slug', 'content', 'description', 'photo', 'get_photo', 'telegram')
    readonly_fields = ('get_photo', )
    save_on_top = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        else:
            return 'no photo'

    get_photo.short_description = 'Фото'


admin.site.register(City, CityAdmin)

admin.site.site_title = 'Управление сайтом'
admin.site.site_header = 'Управление сайтом'

