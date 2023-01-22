from django import template
from blog.models import Tags, Post

register = template.Library()


@register.inclusion_tag('post_tags_tag_tpl.html')
def show_post_tags(post):
    tags = post.tags.all
    print('Tags', tags)
    return {'tags': tags}
