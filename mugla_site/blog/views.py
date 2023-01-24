from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from cities.models import City
from comments.forms import PostCommentForm
from comments.models import PostComments
from .models import Post, Category, Tags
from django.db.models import F, Q
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
        return Post.objects.filter(is_published=True).prefetch_related('tags').select_related('author').order_by('pk')


class Blog(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости'
        return context

    def get_queryset(self):
        return Post.objects.filter(is_published=True).prefetch_related('tags').select_related('author').order_by('pk')


class CategoryPost(Blog):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instance'] = Category.objects.get(slug=self.kwargs['slug'])
        context['title'] = context['instance'].title
        return context

    def get_queryset(self):
        posts = Post.objects.filter(
            Q(category__slug=self.kwargs['slug'])|
            Q(category__slug__in=[i.slug for i in Category.objects.filter(parent__slug=self.kwargs['slug'])])
        )
        return posts.order_by('pk')


class TagPost(Blog):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instance'] = Tags.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug']).order_by('pk')


class CityPost(Blog):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instance'] = City.objects.get(slug=self.kwargs['slug'])
        context['title'] = 'Новости ' + context['instance'].title
        return context

    def get_queryset(self):
        return Post.objects.filter(cities__slug=self.kwargs['slug'])


class PostPage(FormMixin, DetailView):
    model = Post
    context_object_name = 'post'
    allow_empty = False
    form_class = PostCommentForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('post', kwargs={'slug': self.kwargs['slug']})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        messages.success(self.request, f'Ваш комментарий отправлен, он будет опубликован после модерации')
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        context['comments'] = PostComments.objects.filter(Q(post__slug=self.kwargs['slug']) & Q(active=True))
        return context


class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('search'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search")
        context['search'] = f'search={search}&'
        context['title'] = f'Поиск - {search}'
        return context




