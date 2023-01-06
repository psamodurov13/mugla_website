from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django.utils.safestring import mark_safe


class CustomStr():
    def __str__(self):
        if self.title:
            return self.title
        else:
            return self


def dublicate_post(modeladmin, request, queryset):
    '''Function for copy items in admin'''
    for item in queryset:
        model = modeladmin.model

        def pattern_slug(slug):
            return rf'^({slug})' + r'[-]{0,1}\d*'

        def reg_slug(slug):
            return model.objects.filter(slug__iregex=pattern_slug(slug))

        if item.slug.split('-')[-1].isdigit():
            clean_slug = '-'.join(item.slug.split('-')[:-1])
        else:
            clean_slug = item.slug

        # Get all items with clean slug (without digits in the end)
        all_re = reg_slug(clean_slug)
        count = len(all_re)
        item.pk = None
        # Add number in the slug
        item.slug = f'{clean_slug}-{count}'
        item.save()


dublicate_post.short_description = "Дублировать объект"


class CKEditorForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(), label='Контент')


class PrePopulatedSlug(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class BaseAdmin(PrePopulatedSlug, admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_as = True
    save_on_top = True
    actions = [dublicate_post]
    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100">')
        else:
            return '-'

    get_photo.short_description = 'Фото'
