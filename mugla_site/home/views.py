from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from mugla_site import settings
from .models import *
from blog.models import Post
from cities.models import City

# Create your views here.


def view_home(request):
    page = Home.objects.get(slug='home')
    context = {
        'title': page.title,
        'page': page,
        'posts': Post.objects.all().prefetch_related('tags').select_related('author'),
        'cities': City.objects.all(),
        'GOOGLE_MAP_API_KEY': settings.GOOGLE_MAP_API_KEY
    }
    cities_coords = []
    for city in context['cities']:
        if city.location:
            city_info = {'name': city.title, 'description': city.description,
                            'lon': city.location.coords[0], 'lat': city.location.coords[1],
                            'url': city.get_absolute_url()}
            cities_coords.append(city_info)
    context['cities_coords'] = cities_coords
    print(context['cities_coords'])
    return render(request, 'home/index.html', context)
