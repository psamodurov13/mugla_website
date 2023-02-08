from django import template
from blog.models import Post

register = template.Library()


@register.inclusion_tag('footer_tpl.html')
def get_last_posts(cnt=2):
    last_posts = Post.objects.filter(is_published=True).order_by('-created_at')[:cnt]
    return {'last_posts': last_posts}