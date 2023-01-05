from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CustomStr():
    def __str__(self):
        if self.title:
            return self.title
        else:
            return self


class CKEditorForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())


class PrePopulatedSlug(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}


class BaseAdmin(PrePopulatedSlug, admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
