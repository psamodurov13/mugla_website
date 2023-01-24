from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin

from .models import *

from blog.models import Post, Category, Tags
from mugla_site.utils import CKEditorForm, BaseAdmin, dublicate_post
from image_cropping import ImageCroppingMixin


class PostAdminForm(CKEditorForm, forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(ImageCroppingMixin, BaseAdmin):
    form = PostAdminForm
    list_display = ('id', 'title', 'category', 'created_at', 'is_published', 'author')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published', 'category')
    list_filter = ('is_published', 'category', 'author', 'cities')
    fields = ('title', 'slug', 'category', 'content', 'description', 'photo', 'cropping', 'cropping_thumb',
              'get_photo', 'is_published', 'tags', 'cities', 'views', 'created_at', 'author', 'important')
    readonly_fields = ('get_photo', 'views', 'created_at')


class CategoryAdmin(ImageCroppingMixin, BaseAdmin, DraggableMPTTAdmin):
    list_display = ('id', 'title', 'get_photo')


admin.site.register(Tags, BaseAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(
    Category,
    CategoryAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        'get_photo',
        'id'
    ),
    list_display_links=(
        'indented_title',
    ),
)
