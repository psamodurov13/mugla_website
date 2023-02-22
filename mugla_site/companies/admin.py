from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django.utils.safestring import mark_safe
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
from django.contrib.gis.db import models as models_loc
from mapwidgets import GooglePointFieldWidget

from mugla_site.settings import domain
from .models import *

from blog.models import Post, Category, Tags
from mugla_site.utils import CKEditorForm, BaseAdmin, dublicate_post
from image_cropping import ImageCroppingMixin
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin
from mugla_site.tasks import send_html_email_to_user


class CompanyAdminForm(CKEditorForm, forms.ModelForm):

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'location': GooglePointFieldWidget,
        }


class GalleryInline(ImageCroppingMixin, admin.TabularInline):
    fk_name = 'company'
    model = CompanyGallery


CUSTOM_MAP_SETTINGS = {
    "GooglePointFieldWidget": (
        ("zoom", 15),
        ("mapCenterLocation", [60.7177013, -22.6300491]),
    ),
}


class CompanyAdmin(ImageCroppingMixin, BaseAdmin):
    form = CompanyAdminForm
    # formfield_overrides = {
    #     map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    # }
    formfield_overrides = {
        models_loc.PointField: {"widget": GooglePointFieldWidget}
    }
    list_display = ('id', 'title', 'type', 'created_at', 'is_published', 'author')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published', 'type')
    list_filter = ('is_published', 'type', 'author', 'cities')
    fields = ('title', 'slug',
              'location',
              'type', 'content', 'description', 'photo', 'cropping', 'cropping_thumb',
              'get_photo', 'site', 'phone', 'whatsapp', 'telegram', 'note', 'russian_speak', 'english_speak',
              'is_published', 'tags', 'cities', 'views', 'created_at', 'author', 'from_internet')
    readonly_fields = ('get_photo', 'views', 'created_at')
    inlines = [GalleryInline, ]

    def save_model(self, request, obj, form, change):
        if 'is_published' in form.changed_data and obj.is_published == True:
            url = f'{domain}blog/posts/{obj.slug}/'
            send_html_email_to_user.delay(
                obj.author.email,
                'Ваша компания прошла модерацию',
                f'Компания прошла модерацию и доступна по адресу <a href="{url}">{url}</a>'
            )
        obj.save()


class ChangeCompanyAdmin(admin.ModelAdmin):
    readonly_fields = ('company', 'title', 'author', 'content', 'description', 'created_at', 'type', 'tags', 'cities',
                       'site', 'phone', 'whatsapp', 'telegram', 'note', 'russian_speak', 'english_speak')
    list_display = ('company', 'author', 'processed')


class TypeAdmin(ImageCroppingMixin, BaseAdmin, DraggableMPTTAdmin):
    pass


admin.site.register(CompanyTags, BaseAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(ChangeCompany, ChangeCompanyAdmin)
admin.site.register(
    Type,
    TypeAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    ),
)
