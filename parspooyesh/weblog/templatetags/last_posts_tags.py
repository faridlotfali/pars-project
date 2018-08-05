from django import template
from ..models import Post
register = template.Library()


# @register.inclusion_tag('weblog/header.html' , takes_context=True)
@register.inclusion_tag('weblog/last_posts.html')
def last_5post():
    posts = Post.objects.all()[:5]
    return {'posts': posts}