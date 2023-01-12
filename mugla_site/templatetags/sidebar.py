from django import template
from blog.models import Tags, Post

register = template.Library()


@register.inclusion_tag('tags_tpl.html')
def show_tag_list():
    tags = Tags.objects.all()
    return {'tags': tags}


@register.inclusion_tag('popular_posts_tpl.html')
def get_popular(cnt=3):
    posts = Post.objects.order_by('-views')[:cnt]
    return {'posts': posts}
