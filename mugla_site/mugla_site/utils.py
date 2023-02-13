from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.core.mail import send_mail
from django.db import models, IntegrityError
from image_cropping import ImageRatioField
import time
from django.core.mail import EmailMultiAlternatives

from django.utils.safestring import mark_safe

from mugla_site.settings import FROM_EMAIL


class CustomStr():
    def __str__(self):
        if self.title:
            return self.title
        elif self.name:
            return self.name
        else:
            return self


class BaseModel(CustomStr, models.Model):
    slug = models.SlugField(max_length=255, verbose_name='URL', unique=True)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', default='default_post.jpeg', blank=True, verbose_name='Фото')
    cropping = ImageRatioField('photo', '1950x687', size_warning=True, verbose_name='Обрезанное фото для фона')

    class Meta:
        abstract = True


class CustomGallery(models.Model):
    image = models.ImageField(upload_to='company_gallery/%Y/%m/%d/', blank=True, verbose_name='Доп. фото')
    cropping_gallery = ImageRatioField('image', '400x300', size_warning=True, verbose_name='Обрезанное доп фото')

    class Meta:
        abstract = True


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
        try:
            item.slug = f'{clean_slug}-{count}'
            item.save()
        except IntegrityError:
            item.slug = f'{item.slug}-{count}'
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


def send(user_email, subject, text):
    send_mail(subject, text, FROM_EMAIL, [user_email], fail_silently=False)


def send_html_email(user_email, subject, text):
    msg = EmailMultiAlternatives(subject=subject, from_email=FROM_EMAIL, to=[user_email])
    msg.attach_alternative(text, "text/html")
    msg.send()


def get_subcategories(all_categories, head_category):
    head_category_id = all_categories.get(title=head_category).id
    subcategories_id = [i.id for i in all_categories.filter(parent=head_category_id)]
    subcategories_id.append(head_category_id)
    return all_categories.filter(parent__in=subcategories_id)
