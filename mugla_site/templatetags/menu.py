from django import template
from blog.models import show_categories
from cities.models import show_cities
from companies.models import show_company_types
from mugla_site.utils import get_subcategories

register = template.Library()


@register.inclusion_tag('menu_tpl.html')
def show_menu():
    all_categories = show_categories()
    news = get_subcategories(all_categories, 'Новости')
    print(news)
    articles = get_subcategories(all_categories, 'Статьи')
    print(articles)
    cities = show_cities()
    company_types = show_company_types()

    return {'news': news, 'articles': articles, 'cities': cities, 'company_types': company_types}

