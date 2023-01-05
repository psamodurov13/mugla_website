from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django.utils.safestring import mark_safe
from .models import *

from blog.models import Post, Category, Tags
from mugla_site.utils import CKEditorForm, BaseAdmin


class PostAdminForm(CKEditorForm, forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(BaseAdmin, admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('id', 'title', 'category', 'created_at', 'is_published', 'author')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published', 'category')
    list_filter = ('is_published', 'category', 'author', 'cities')
    fields = ('title', 'slug', 'category', 'content', 'description', 'photo', 'get_photo', 'is_published', 'tags',
              'cities', 'views', 'created_at', 'author')
    readonly_fields = ('get_photo', 'views', 'created_at')
    save_on_top = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        else:
            return 'no photo'

    get_photo.short_description = 'Фото'


admin.site.register(Category, BaseAdmin)
admin.site.register(Tags, BaseAdmin)
admin.site.register(Post, PostAdmin)
