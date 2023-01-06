from django import template
from blog.models import show_tags

register = template.Library()


@register.inclusion_tag('tags_tpl.html')
def show_tag_list():
    tags = show_tags()
    return {'tags': tags}