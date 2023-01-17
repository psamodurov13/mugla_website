from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from .models import *
from blog.models import Post

# Create your views here.


def view_home(request):
    page = Home.objects.get(slug='home')
    context = {
        'title': page.title,
        'page': page,
        'posts': Post.objects.all()
    }
    return render(request, 'home/index.html', context)
