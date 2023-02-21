from django import template
from blog.models import show_categories
from cities.models import show_cities, get_regions, filter_cities_by_region
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
    regions = get_regions()
    cities_by_regions = []
    for region in regions:
        region_dict = {}
        region_dict['name'] = region
        region_dict['cities'] = filter_cities_by_region(region)
        cities_by_regions.append(region_dict)
    print(f'CITIES BY REGIONS - {cities_by_regions}')

    return {'news': news, 'articles': articles, 'cities': cities, 'company_types': company_types,
            'cities_by_regions': cities_by_regions}

