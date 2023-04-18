from django.shortcuts import render

# Create your views here.
from mugla_site import settings
from mugla_site.configs import YOUR_MAPBOX_ACCESS_TOKEN


def default_map(request):
    return render(request, 'maps/default_map.html', {'title': 'Map Time!',
                                                     'YOUR_MAPBOX_ACCESS_TOKEN': YOUR_MAPBOX_ACCESS_TOKEN,
                                                     'GOOGLE_MAP_API_KEY': settings.GOOGLE_MAP_API_KEY})