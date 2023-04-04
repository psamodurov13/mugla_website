# import os
#
# import django
# from django.core.wsgi import get_wsgi_application
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mugla_site.settings")
#
# application = get_wsgi_application()
# django.setup()
# from django.conf import settings
# settings.configure()
# from mugla_site.wsgi import *
# from django.core.management import call_command
from django.contrib import admin
from .models import CollectData
from loguru import logger
from mugla_site.tasks import load_companies_task
from collect_data.load import load_companies
from collect_data.collect import collect_data
# from mugla_site.tasks import load_companies_task
# from .collect import collect_data
from cities.models import City


class CollectDataAdmin(admin.ModelAdmin):
    list_display = ('query', 'city', 'date', 'collect_status')
    search_fields = ('query', 'city')
    fields = ('query', 'city', 'url')

    def save_model(self, request, obj, form, change):
        logger.info(f'OBJ - {obj.__dict__}')
        logger.info(f'FORM - {form.__dict__}')
        # collect_data(obj.url, obj.city.title)
        obj.collect_status = 'В процессе'
        obj.save()
        load_companies_task.delay(obj.url, obj.city.title, obj.query, obj.id)


admin.site.register(CollectData, CollectDataAdmin)

