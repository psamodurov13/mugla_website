from django.contrib import admin

# Register your models here.
from django import forms
from image_cropping import ImageCroppingMixin

from home.models import Home
from mugla_site.utils import CKEditorForm, BaseAdmin


# Register your models here.
class HomeAdminForm(CKEditorForm, forms.ModelForm):

    class Meta:
        model = Home
        fields = '__all__'


class HomeAdmin(ImageCroppingMixin, BaseAdmin):
    form = HomeAdminForm
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


admin.site.register(Home, HomeAdmin)
