from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='cities'),
    path('regions/<str:slug>/', RegionPage.as_view(), name='region'),
    path('regions/', RegionListPage.as_view(), name='regions'),
    path('city/<str:slug>/', CityPage.as_view(), name='city'),
    path('city/<str:slug>/gallery/', CityGalleryPage.as_view(), name='city_gallery'),
]