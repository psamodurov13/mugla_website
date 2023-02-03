from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django.utils.safestring import mark_safe
from image_cropping import ImageCroppingMixin
from mapwidgets import GooglePointFieldWidget


from .models import *
from mugla_site.utils import BaseAdmin

from mugla_site.utils import CKEditorForm


# Register your models here.
class CityAdminForm(CKEditorForm, forms.ModelForm):

    class Meta:
        model = City
        fields = '__all__'


class GalleryInline(ImageCroppingMixin, admin.TabularInline):
    fk_name = 'city'
    model = CityGallery


class CityAdmin(ImageCroppingMixin, BaseAdmin):
    form = CityAdminForm
    formfield_overrides = {
        models_loc.PointField: {"widget": GooglePointFieldWidget}
    }
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    fields = ('title', 'slug', 'content', 'description', 'location', 'photo', 'cropping', 'get_photo', 'telegram',
              'populate',
              'distance_to_airport', 'content_photo', 'cropping_content_photo')
    inlines = [GalleryInline, ]


admin.site.register(City, CityAdmin)

admin.site.site_title = 'Управление сайтом'
admin.site.site_header = 'Управление сайтом'

