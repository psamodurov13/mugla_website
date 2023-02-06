from django.contrib import admin
from .models import *

# Register your models here.


class FeedbackCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']


class FeedbackMessageAdmin(admin.ModelAdmin):
    readonly_fields = ['title', 'category', 'email', 'text']
    list_display = ['title', 'category', 'processed']


admin.site.register(FeedbackCategory, FeedbackCategoryAdmin)
admin.site.register(FeedbackMessage, FeedbackMessageAdmin)
