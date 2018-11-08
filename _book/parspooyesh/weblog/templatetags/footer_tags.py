from django import template
from ..models import SiteSettings
register = template.Library()


@register.inclusion_tag('weblog/footer.html' , takes_context=True)
def footer(context):
    pass

@register.filter(name='footer_settings')
def footer_settings(value,args = None):
    footer = ''
    if SiteSettings.objects.all().filter(key_name__iexact=value):
        footer= SiteSettings.objects.all().filter(key_name=value)[0].key_value
    return footer