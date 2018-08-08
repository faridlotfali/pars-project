from django import template
from ..models import Post
register = template.Library()


# @register.inclusion_tag('weblog/header.html' , takes_context=True)
@register.inclusion_tag('weblog/last_posts.html')
def last_post():
    posts = Post.objects.all()[:3]
    return {'posts': posts}