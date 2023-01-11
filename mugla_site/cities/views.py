from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView
from cities.models import City


def index(request):
    return render(request, 'cities/index.html')


class CityPage(DetailView):
    model = City
    context_object_name = 'city'
