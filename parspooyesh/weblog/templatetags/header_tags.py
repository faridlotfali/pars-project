from django import template
from ..models import Post,SiteSettings
register = template.Library()


@register.inclusion_tag('weblog/header.html' , takes_context=True)
def header(context):
    # header_title = SiteSetting.objects.all().first().header_title
    topsearch = None
    request = context["request"]
    topsearch_text = request.GET.get('text')
    if topsearch_text : 
        topsearch = Post.objects.filter(post_text__icontains=topsearch_text) 
    return {'topsearch': topsearch , 'user':request.user }

@register.filter(name='header_settings')
def header_settings(value,args):
    header_title = SiteSettings.objects.all().filter(key_name='header').first().key_value
    return header_title