from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'cities/index.html')


def get_city(request, slug):
    return render(request, 'cities/city.html')
