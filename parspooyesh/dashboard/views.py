from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.contrib.auth.models import User

from weblog.models import Post,Comment,slider

# @login_required

@login_required(login_url='/weblog/login/')
def index(request):        
    user_post_list = Post.objects.filter(author_id = request.user.id).order_by('-pub_date')[:5]
    context = {
        'user_post_list': user_post_list,
    }
    return  render(request,'dashboard2/index.html',context)
