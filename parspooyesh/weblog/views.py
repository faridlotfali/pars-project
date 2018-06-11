from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404
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



def detail(request,post_id):
    # try:
    #    post = Post.objects.get(pk=post_id)
    # except Post.DoesNotExist:
        # raise Http404("post does not exist") #next line is shortcut
    post = get_object_or_404(Post, pk=post_id) 
    return render(request, 'weblog/detail.html', {'post':post})


def results(request, post_id):
    response = "You're looking at the results of post %s."
    return HttpResponse(response % post_id)


def vote(request, post_id):
    return HttpResponse("You're commenting on post %s." % post_id)