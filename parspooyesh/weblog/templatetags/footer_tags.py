from django import template
from ..models import Post
register = template.Library()


@register.inclusion_tag('weblog/footer.html')
def footer():
    posts = Post.objects.all()[:5]
    return {'posts': posts}