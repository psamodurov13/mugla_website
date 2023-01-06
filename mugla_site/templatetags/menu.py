from django import template
from blog.models import show_categories
from cities.models import show_cities

register = template.Library()


@register.inclusion_tag('menu_tpl.html')
def show_menu():
    categories = show_categories()
    cities = show_cities()
    return {'categories': categories, 'cities': cities}

