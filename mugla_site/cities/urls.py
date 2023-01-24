from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='cities'),
    path('city/<str:slug>/', CityPage.as_view(), name='city'),
    path('city/<str:slug>/gallery/', CityGalleryPage.as_view(), name='city_gallery'),
]