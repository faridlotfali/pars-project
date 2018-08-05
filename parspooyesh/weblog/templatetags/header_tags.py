from django import template
from ..models import Post
register = template.Library()


@register.inclusion_tag('weblog/header.html' , takes_context=True)
def header(context):
    topsearch = None
    topsearch_text = context["request"].GET.get('text')
    if topsearch_text : 
        topsearch = Post.objects.filter(post_text__icontains=topsearch_text) 
    return {'topsearch': topsearch}