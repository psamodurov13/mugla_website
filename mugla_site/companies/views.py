from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, CreateView

from cities.models import City
from comments.forms import PostCommentForm, CompanyCommentForm
from comments.models import CompanyComments
from .models import Type, CompanyTags, Company, CompanyGallery
from django.db.models import F, Q
from .forms import *
from transliterate import slugify
from image_cropping.utils import get_backend


class CompaniesList(ListView):
    model = Company
    template_name = 'companies/companies.html'
    context_object_name = 'companies'
    paginate_by = 4
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Компании'
        return context

    def get_queryset(self):
        return Company.objects.filter(is_published=True).prefetch_related('tags').select_related('author').order_by('pk')


class TypeCompany(CompaniesList):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instance'] = Type.objects.get(slug=self.kwargs['slug'])
        context['title'] = context['instance'].title
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
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        context['gallery'] = CompanyGallery.objects.filter(company=self.object.id)
        context['comments'] = CompanyComments.objects.filter(Q(company__slug=self.kwargs['slug']) & Q(active=True))
        return context


class CreateCompany(LoginRequiredMixin, CreateView):
    form_class = CreateCompanyForm
    template_name = 'companies/create_company.html'
    login_url = '/login/'
    success_url = reverse_lazy('create_company')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        last_id = Company.objects.order_by('id').last().id
        slug = slugify(self.object.title, language_code='ru')
        self.object.slug = f'{slug}-{str(last_id + 1)}'
        self.object.save()
        for i in form.files.getlist('file_field'):
            item = CompanyGallery()
            item.image = i
            item.company = self.object
            item.save()
        messages.success(self.request, 'Организация добавлена, она будет опубликована после модерации. Спасибо')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateCompany, self).get_context_data(**kwargs)
        context['title'] = 'Создание организации'
        return context







