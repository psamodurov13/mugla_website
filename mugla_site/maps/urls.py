from django.urls import path

from .views import *

urlpatterns = [
    path('', default_map, name='maps'),
]