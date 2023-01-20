from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from cities.models import City
from .models import Type, CompanyTags, Company, CompanyGallery
from django.db.models import F, Q
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
            Q(type__slug=self.kwargs['slug']) |
            Q(type__slug__in=[i.slug for i in Type.objects.filter(parent__slug=self.kwargs['slug'])])
        )
        return companies.prefetch_related('tags').select_related('author').order_by('pk')


class TagCompany(CompaniesList):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instance'] = CompanyTags.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        return Company.objects.filter(tags__slug=self.kwargs['slug']).prefetch_related(
            'tags').select_related('author').order_by('pk')


class CityCompanies(CompaniesList):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instance'] = City.objects.get(slug=self.kwargs['slug'])
        context['title'] = 'Новости ' + context['instance'].title
        return context

    def get_queryset(self):
        return Company.objects.filter(cities__slug=self.kwargs['slug']).prefetch_related('tags').select_related('author')


class CompanyPage(DetailView):
    model = Company
    context_object_name = 'company'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        context['gallery'] = CompanyGallery.objects.filter(company=self.object.id)
        return context






