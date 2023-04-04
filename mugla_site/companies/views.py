from crispy_forms.utils import render_crispy_form
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, CreateView

from cities.models import City
from users.models import User
from comments.forms import PostCommentForm, CompanyCommentForm
from comments.models import CompanyComments
from mugla_site import settings
from mugla_site.utils import get_subcategories
from .models import Type, CompanyTags, Company, CompanyGallery
from django.db.models import F, Q
from .forms import *
from transliterate import slugify
from jsonview.decorators import json_view
from django.template.context_processors import csrf
from image_cropping.utils import get_backend
from mugla_site.tasks import send_html_email_to_user
from loguru import logger


class CompaniesList(ListView):
    model = Company
    template_name = 'companies/companies.html'
    context_object_name = 'companies'
    paginate_by = 4
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Компании'
        context['categories'] = Type.objects.all()
        return context

    def get_queryset(self):
        return Company.objects.filter(is_published=True).prefetch_related('tags').select_related('author').order_by('pk')


class TypeCompany(CompaniesList):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instance'] = Type.objects.get(slug=self.kwargs['slug'])
        context['title'] = context['instance'].title
        context['categories'] = Type.objects.all()
        breadcrumbs = Type.objects.get(slug=self.kwargs["slug"]).get_ancestors(ascending=False, include_self=True)
        print('bread', breadcrumbs)
        breadcrumbs = breadcrumbs[:len(breadcrumbs) - 1]
        context['breadcrumbs'] = breadcrumbs
        context['check'] = True
        return context

    def get_queryset(self):
        companies = Company.objects.filter(
            Q(type__in=Type.objects.get(slug=self.kwargs['slug']).get_descendants(include_self=True)) &
            Q(is_published=True)
        )
        return companies.prefetch_related('tags').select_related('author').order_by('pk')


class TagCompany(CompaniesList):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instance'] = CompanyTags.objects.get(slug=self.kwargs['slug'])
        context['title'] = context['instance'].title
        context['check'] = True
        return context

    def get_queryset(self):
        return Company.objects.filter(Q(tags__slug=self.kwargs['slug']) & Q(is_published=True)).prefetch_related(
            'tags').select_related('author').order_by('pk')


class CityCompanies(CompaniesList):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instance'] = City.objects.get(slug=self.kwargs['slug'])
        context['title'] = 'Организации в городе ' + context['instance'].title
        return context

    def get_queryset(self):
        return Company.objects.filter(Q(cities__slug=self.kwargs['slug']) & Q(is_published=True)).prefetch_related('tags').select_related('author')


class UserCompanies(CompaniesList):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instance'] = User.objects.get(username=self.kwargs['slug'])
        context['title'] = 'Организации добавленные пользователем ' + context['instance'].username
        return context

    def get_queryset(self):
        return Company.objects.filter(Q(author__username=self.kwargs['slug']) &
                                      Q(is_published=True)).prefetch_related('tags').select_related('author')


class CompanyPage(FormMixin, DetailView):
    model = Company
    context_object_name = 'company'
    allow_empty = False
    form_class = CompanyCommentForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('company', kwargs={'slug': self.kwargs['slug']})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.company = self.get_object()
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
        logger.info(f'KWARGS - {City.objects.filter(companies=self.object.id)}')
        context['gallery'] = CompanyGallery.objects.filter(Q(company=self.object.id) & Q(is_published=True))
        context['comments'] = CompanyComments.objects.filter(Q(company__slug=self.kwargs['slug']) & Q(active=True))
        context['cities'] = City.objects.filter(companies=self.object.id)
        context['add_photo_form'] = AddCompanyPhoto()
        context['change_company_form'] = ChangeCompanyForm()
        breadcrumbs = self.object.type.get_ancestors(ascending=False, include_self=True)
        context['breadcrumbs'] = breadcrumbs
        context['GOOGLE_MAP_API_KEY'] = settings.GOOGLE_MAP_API_KEY
        if context['company'].location:
            context['company'].longitude = str(context['company'].location.coords[0])
            context['company'].latitude = str(context['company'].location.coords[1])
        # print(f'Location - {self.object.location}\n{"-"*40}\n{dir(self.object.location)}\n{self.object.location[0]}')
        return context


@json_view
def create_company_ajax(request):
    if request.method == 'POST':
        form = CreateCompanyForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.__dict__)
            print(form.cleaned_data)
            form_data = form.cleaned_data
            tags_data = form_data['tags']
            form_data.pop('tags')
            form_data['author'] = request.user
            cities_data = form_data['cities']
            gallery = form.files.getlist('gallery_images')
            form_data.pop('cities')
            form_data.pop('gallery_images')
            form_data.pop('captcha')
            last_id = Company.objects.order_by('id').last().id
            slug = slugify(form_data['title'], language_code='ru') + str(last_id + 1)
            form_data['slug'] = slug
            new_company = Company.objects.create(**form_data)
            print(f'NEW {new_company} - {new_company.__dict__}')
            new_company.tags.set(tags_data)
            new_company.cities.set(cities_data)
            print(f'DATA - {new_company}')
            new_company.save()
            for image in gallery:
                print(image)
                item = CompanyGallery()
                item.image = image
                item.company = new_company
                item.save()
            url = f'http://{request.META["HTTP_HOST"]}/companies/company/{new_company.slug}/'
            send_html_email_to_user.delay(
                request.user.email,
                'Ваша компания отправлена на модерацию',
                f'Благодарим Вас за добавление компании. Она будет доступна по адресу <a href="{url}">{url}</a> '
                f'после прохождения модерации'
            )
            messages.success(request, 'Организация добавлена')
            return JsonResponse({'error': False, 'message': 'Компания добавлена'})
        else:
            # messages.error(request, 'Есть ошибки')
            return JsonResponse({'error': True, 'errors': form.errors, 'message': 'Проверьте форму'})
    else:
        form = CreateCompanyForm()
        title = 'Добавить компанию'
        check = True
        return render(request, 'companies/create_company.html', {'form': form, 'title': title, 'check': check})


@json_view
def add_photo_ajax(request):
    if request.method == 'POST':
        form = AddCompanyPhoto(request.POST, request.FILES)
        if form.is_valid():
            print('FORM', form.__dict__)
            print('FORM CLEAN', form.cleaned_data)
            print('REQUEST', dir(request))
            print('REQUEST', request.META['HTTP_REFERER'])
            print('INSTANCE', form.instance.__dict__)
            form_data = form.cleaned_data

            gallery = form.files.getlist('gallery_images')
            form_data.pop('gallery_images')
            for image in gallery:
                print(image)
                item = CompanyGallery()
                item.image = image
                item.company = Company.objects.get(slug=request.META['HTTP_REFERER'].split('/')[-1])
                item.is_published = False
                item.save()

            messages.success(request, 'Фото добавлены')
            return JsonResponse({'error': False, 'message': 'Фото добавлены'})
        else:
            return JsonResponse({'error': True, 'errors': form.errors, 'message': 'Проверьте форму'})


@json_view
def change_company_ajax(request):
    if request.method == 'POST':
        form = ChangeCompanyForm(request.POST)
        if form.is_valid():
            print('FORM', form.__dict__)
            print('FORM CLEAN', form.cleaned_data)
            print('REQUEST', dir(request))
            print('REQUEST', request.META['HTTP_REFERER'])
            print('INSTANCE', form.instance.__dict__)
            form_data = form.cleaned_data
            tags_data = form_data['tags']
            form_data.pop('tags')
            form_data['author'] = request.user
            cities_data = form_data['cities']
            form_data.pop('cities')
            slug = request.META['HTTP_REFERER'].split('/')[-1]
            company = Company.objects.get(slug=slug)
            form_data['company'] = company
            form_data['processed'] = False
            new_edition = ChangeCompany.objects.create(**form_data)
            print(f'NEW {new_edition} - {new_edition.__dict__}')
            new_edition.tags.set(tags_data)
            new_edition.cities.set(cities_data)
            print(f'DATA - {new_edition}')
            new_edition.save()

            messages.success(request, 'Изменения добавлены')
            return JsonResponse({'error': False, 'message': 'Изменения добавлены'})
        else:
            return JsonResponse({'error': True, 'errors': form.errors, 'message': 'Проверьте форму'})







