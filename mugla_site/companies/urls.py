from django.urls import path

from .views import *

urlpatterns = [
    path('', CompaniesList.as_view(), name='companies'),
    path('create-company/', CreateCompany.as_view(), name='create_company'),
    path('create-company-ajax/', create_company_ajax, name='create_company_ajax'),
    path('type/<str:slug>', TypeCompany.as_view(), name='type'),
    path('company/<str:slug>', CompanyPage.as_view(), name='company'),
    path('company-tags/<str:slug>', TagCompany.as_view(), name='company-tags'),
    path('<str:slug>/', CityCompanies.as_view(), name='city_companies'),
]