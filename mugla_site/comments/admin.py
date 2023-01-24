from django.contrib import admin
from django import forms

from comments.models import *
from mugla_site.utils import CKEditorForm, BaseAdmin

# Register your models here.

#
# class PostCommentsAdminForm(forms.ModelForm):
#
#     class Meta:
#         model = PostComments
#         fields = '__all__'
#
#
# class CompanyCommentsAdminForm(forms.ModelForm):
#
#     class Meta:
#         model = CompanyComments
#         fields = '__all__'
#
#


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'author', 'created_at', 'active')
    list_display_links = ('id', )
    search_fields = ('content', )
    list_editable = ('active', )
    list_filter = ('active', 'author')
    fields = ('content', 'author', 'created_at', 'active')
    readonly_fields = ('created_at', )


class PostCommentsAdmin(CommentsAdmin):
    fields = ('post', 'content', 'author', 'created_at', 'active')


class CompanyCommentsAdmin(CommentsAdmin):
    fields = ('company', 'content', 'author', 'created_at', 'active')


admin.site.register(PostComments, PostCommentsAdmin)
admin.site.register(CompanyComments, CompanyCommentsAdmin)

