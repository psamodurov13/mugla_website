from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView, View, ListView
from cities.models import City
from blog.models import Post
from companies.models import Company
from mugla_site import settings
from .models import *
import json


def index(request):
    return render(request, 'cities/index.html')


class CityPage(DetailView):
    model = City
    context_object_name = 'city'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['posts'] = Post.objects.filter(cities=self.object.pk).prefetch_related('tags').select_related('author')
        context['companies'] = Company.objects.filter(cities=self.object.pk).prefetch_related('tags').select_related('author')
        context['gallery'] = CityGallery.objects.filter(city=self.object.id)
        context['articles'] = Post.objects.filter(important=True)
        context['GOOGLE_MAP_API_KEY'] = settings.GOOGLE_MAP_API_KEY

        # context['coords'] = [(str(comp.location.coords[0]), str(comp.location.coords[1])) for comp in context['companies'] if comp.location]
        if context['city'].location:
            context['city'].longitude = str(context['city'].location.coords[0])
            context['city'].latitude = str(context['city'].location.coords[1])
            companies_coords = []
            for company in context['companies']:
                if company.location:
                    company_info = {'name': company.title, 'description': company.description,
                                    'lon': company.location.coords[0], 'lat': company.location.coords[1],
                                    'url': company.get_absolute_url()}
                    companies_coords.append(company_info)
            context['companies_coords'] = companies_coords
        print('LOC', context['city'].__dict__)
        # print('CITY LOCATIONS', context['coords'])
        return self.render_to_response(context)


class CityGalleryPage(ListView):
    model = CityGallery
    context_object_name = 'gallery'
    template_name = 'cities/city_gallery.html'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = City.objects.get(slug=self.kwargs['slug'])
        return context

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     context = self.get_context_data(object=self.object)
    #     context['gallery'] = CityGallery.objects.filter(city=self.object.id)
    #     return self.render_to_response(context)




