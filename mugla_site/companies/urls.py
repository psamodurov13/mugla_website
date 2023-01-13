from django.urls import path

from .views import *

urlpatterns = [
    path('', CompaniesList.as_view(), name='companies'),
    path('type/<str:slug>', TypeCompany.as_view(), name='type'),
    path('company/<str:slug>', CompanyPage.as_view(), name='company'),
]