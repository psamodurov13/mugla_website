from django import template
from blog.models import show_categories
from cities.models import show_cities
from companies.models import show_company_types

register = template.Library()


@register.inclusion_tag('menu_tpl.html')
def show_menu():
    categories = show_categories()
    cities = show_cities()
    company_types = show_company_types()
    return {'categories': categories, 'cities': cities, 'company_types': company_types}

