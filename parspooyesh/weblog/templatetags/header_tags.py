from django.shortcuts import render,redirect
from django import template
from datetime import datetime
from ..models import Post,SiteSettings
register = template.Library()


@register.inclusion_tag('weblog/header.html' , takes_context=True)
def header(context):
    request = context["request"]
    return {'user': request.user }

@register.filter(name='header_settings')
def header_settings(value,args=None):
    header_title = SiteSettings.objects.all().filter(key_name='header').first().key_value
    return header_title
