from django.urls import path

from .views import *

urlpatterns = [
    path('', view_home, name='home'),
]