from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, CreateView

from cities.models import City
from users.models import User
from comments.forms import PostCommentForm
from comments.models import PostComments
from mugla_site.utils import get_subcategories
from .forms import CreatePostForm
from .models import Post, Category, Tags, show_categories
from django.db.models import F, Q
from transliterate import slugify
from jsonview.decorators import json_view
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
        all_categories = show_categories()
        breadcrumbs = Category.objects.get(slug=self.kwargs["slug"]).get_ancestors(ascending=False, include_self=True)
        context['categories'] = get_subcategories(all_categories, breadcrumbs[0].title)
        breadcrumbs = breadcrumbs[:len(breadcrumbs) - 1]
        context['breadcrumbs'] = breadcrumbs
        return context

    def get_queryset(self):
        posts = Post.objects.filter(
            Q(category__in=Category.objects.get(slug=self.kwargs['slug']).get_descendants(include_self=True)) &
            Q(is_published=True)
        ).prefetch_related('tags').select_related('author')
        return posts.order_by('pk')


class TagPost(Blog):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instance'] = Tags.objects.get(slug=self.kwargs['slug'])
        context['title'] = context['instance'].title
        return context

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'] & Q(is_published=True)).order_by('pk')


class CityPost(Blog):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instance'] = City.objects.get(slug=self.kwargs['slug'])
        context['title'] = 'Новости ' + context['instance'].title
        all_categories = show_categories()
        breadcrumbs = Category.objects.get(title='Новости').get_ancestors(ascending=False, include_self=True)
        context['categories'] = get_subcategories(all_categories, breadcrumbs[0].title)
        breadcrumbs = breadcrumbs[:len(breadcrumbs) - 1]
        context['breadcrumbs'] = breadcrumbs
        return context

    def get_queryset(self):
        return Post.objects.filter(cities__slug=self.kwargs['slug'] & Q(is_published=True))


class UserNews(Blog):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instance'] = User.objects.get(username=self.kwargs['slug'])
        context['title'] = 'Новости пользователя ' + context['instance'].username
        all_categories = show_categories()
        context['categories'] = get_subcategories(all_categories, 'Новости')
        context['breadcrumbs'] = []
        return context

    def get_queryset(self):
        return Post.objects.filter(Q(author__username=self.kwargs['slug']) &
                                   Q(category__in=Category.objects.get(title='Новости')
                                     .get_descendants(include_self=True)) & Q(is_published=True))


class UserArticles(Blog):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instance'] = User.objects.get(username=self.kwargs['slug'])
        context['title'] = 'Статьи пользователя ' + context['instance'].username
        all_categories = show_categories()
        context['categories'] = get_subcategories(all_categories, 'Статьи')
        context['breadcrumbs'] = []
        return context

    def get_queryset(self):
        return Post.objects.filter(Q(author__username=self.kwargs['slug']) &
                                   Q(category__in=Category.objects.get(title='Статьи')
                                     .get_descendants(include_self=True)) & Q(is_published=True))


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
        return JsonResponse({'error': False, 'message': 'Комментарий добавлен'})

    def form_invalid(self, form):
        return JsonResponse({'error': True, 'errors': form.errors, 'message': 'Проверьте форму'})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        context['comments'] = PostComments.objects.filter(Q(post__slug=self.kwargs['slug']) & Q(active=True))
        breadcrumbs = self.object.category.get_ancestors(ascending=False, include_self=True)
        context['breadcrumbs'] = breadcrumbs
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


# class CreatePost(LoginRequiredMixin, CreateView):
#     form_class = CreatePostForm
#     template_name = 'blog/create_post.html'
#     login_url = '/login/'
#     success_url = reverse_lazy('create_post')
#
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.author = self.request.user
#         last_id = Post.objects.order_by('id').last().id
#         slug = slugify(self.object.title, language_code='ru')
#         self.object.slug = f'{slug}-{str(last_id + 1)}'
#         self.object.save()
#         messages.success(self.request, 'Пост добавлен, он будет опубликован после модерации. Спасибо')
#         return super().form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super(CreatePost, self).get_context_data(**kwargs)
#         context['title'] = 'Создание поста'
#         return context



@json_view
def create_post_ajax(request):

    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.__dict__)
            print(form.cleaned_data)
            form_data = form.cleaned_data
            tags_data = form_data['tags']
            form_data.pop('tags')
            form_data['author'] = request.user
            cities_data = form_data['cities']
            form_data.pop('cities')
            form_data.pop('captcha')
            last_id = Post.objects.order_by('id').last().id
            slug = slugify(form_data['title'], language_code='ru') + str(last_id + 1)
            form_data['slug'] = slug
            new_post = Post.objects.create(**form_data)
            print(f'NEW {new_post} - {new_post.__dict__}')
            new_post.tags.set(tags_data)
            new_post.cities.set(cities_data)
            print(f'DATA - {new_post}')
            new_post.save()
            messages.success(request, 'Пост добавлен')
            return JsonResponse({'error': False, 'message': 'Пост добавлен'})
        else:
            # messages.error(request, 'Есть ошибки')
            return JsonResponse({'error': True, 'errors': form.errors, 'message': 'Проверьте форму'})
    else:
        form = CreatePostForm()
        title = 'Добавить пост'
        return render(request, 'blog/create_post.html', {'form': form, 'title': title})






