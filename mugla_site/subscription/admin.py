from django.contrib import admin

# Register your models here.
from subscription.models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date')


admin.site.register(Subscription, SubscriptionAdmin)
