from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView, View, ListView
from cities.models import City
from blog.models import Post
from companies.models import Company
from .models import *


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




