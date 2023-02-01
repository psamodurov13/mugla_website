from django import template
from blog.models import Tags, Post
from companies.models import CompanyTags, Company

register = template.Library()


@register.inclusion_tag('tags_tpl.html')
def show_tag_list():
    tags = Tags.objects.all()
    return {'tags': tags}


@register.inclusion_tag('tags_tpl.html')
def show_company_tag_list():
    tags = CompanyTags.objects.all()
    return {'tags': tags}


@register.inclusion_tag('popular_posts_tpl.html')
def get_popular(cnt=3):
    posts = Post.objects.order_by('-views')[:cnt]
    return {'posts': posts}


@register.inclusion_tag('popular_posts_tpl.html')
def get_popular_company(cnt=3):
    posts = Company.objects.order_by('-views')[:cnt]
    return {'posts': posts}


@register.inclusion_tag('sidebar_menu_tpl.html')
def get_categories_menu(categories):
    return {'categories': categories}
