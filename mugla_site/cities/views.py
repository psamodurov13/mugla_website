from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView
from cities.models import City
from blog.models import Post


def index(request):
    return render(request, 'cities/index.html')


class CityPage(DetailView):
    model = City
    context_object_name = 'city'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['posts'] = Post.objects.filter(cities=self.object.pk).prefetch_related('tags').select_related('author')
        return self.render_to_response(context)
