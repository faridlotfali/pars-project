from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Post

def index(request):
    latest_post_list = Post.objects.order_by('-pub_date')[:5]
    # output = ', '.join([p.post_text for p in latest_post_list])
    # return HttpResponse(output)
    # template = loader.get_template('weblog/index.html') next code is shortcut
    context = {
        'latest_post_list': latest_post_list,
    }
    # return HttpResponse(template.render(ontext,request)) next code is shortcut
    return  render(request,'weblog/index.html',context)



def detail(request, post_id):
    return HttpResponse("You're looking at question %s." % post_id)


def results(request, post_id):
    response = "You're looking at the results of post %s."
    return HttpResponse(response % post_id)


def vote(request, post_id):
    return HttpResponse("You're commenting on post %s." % post_id)