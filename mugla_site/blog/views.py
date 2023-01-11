from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tags
from image_cropping.utils import get_backend


class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Последние новости'
        return context

    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('pk')


class Blog(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости'
        return context

    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('pk')


class CategoryPost(Blog):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instance'] = Category.objects.get(slug=self.kwargs['slug'])
        context['title'] = context['instance'].title
        return context

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug']).order_by('pk')


class TagPost(Blog):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instance'] = Tags.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        print(self.__dict__)
        return Post.objects.filter(tags__slug=self.kwargs['slug']).order_by('pk')


class PostPage(DetailView):
    model = Post
    context_object_name = 'post'

