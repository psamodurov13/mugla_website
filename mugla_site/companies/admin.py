from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django.utils.safestring import mark_safe
from .models import *

from blog.models import Post, Category, Tags
from mugla_site.utils import CKEditorForm, BaseAdmin, dublicate_post
from image_cropping import ImageCroppingMixin


class CompanyAdminForm(CKEditorForm, forms.ModelForm):

    class Meta:
        model = Company
        fields = '__all__'


class GalleryInline(ImageCroppingMixin, admin.TabularInline):
    fk_name = 'company'
    model = CompanyGallery


class CompanyAdmin(ImageCroppingMixin, BaseAdmin):
    form = CompanyAdminForm
    list_display = ('id', 'title', 'type', 'created_at', 'is_published', 'author')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published', 'type')
    list_filter = ('is_published', 'type', 'author', 'cities')
    fields = ('title', 'slug', 'type', 'content', 'description', 'photo', 'cropping', 'cropping_thumb',
              'get_photo', 'site', 'phone', 'whatsapp', 'telegram', 'note', 'russian_speak', 'english_speak',
              'is_published', 'tags', 'cities', 'views', 'created_at', 'author')
    readonly_fields = ('get_photo', 'views', 'created_at')
    inlines = [GalleryInline, ]


class TypeAdmin(ImageCroppingMixin, BaseAdmin):
    list_display = ('id', 'title', 'parent')

    def get_form(self, request, obj=None, **kwargs):
        form = super(TypeAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['parent'].queryset = Type.objects.exclude(title=obj)
        return form


admin.site.register(Type, TypeAdmin)
admin.site.register(CompanyTags, BaseAdmin)
admin.site.register(Company, CompanyAdmin)
