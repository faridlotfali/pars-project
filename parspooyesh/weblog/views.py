from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.decorators import login_required

from .models import Post,Comment,slider

def index(request):
    latest_post_list = Post.objects.order_by('-pub_date')[:5]
    slide = []
    for data in slider.objects.all(): 
        # slide = Post.objects.filter(pk = data)
        print( list(Post.objects.filter(pk = data.image_id)) ) 
        slide.append (list(Post.objects.filter(pk = data.image_id))[0] )
    # slide = Post.objects.filter(pk = 1)
    # output = ', '.join([p.post_text for p in latest_post_list])
    # return HttpResponse(output)
    # template = loader.get_template('weblog/index.html') next code is shortcut
    context = {
        'latest_post_list': latest_post_list,
        'slider' : slide,
    }
    # return HttpResponse(template.render(context,request)) next code is shortcut
    return  render(request,'weblog/index.html',context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('weblog:index')
    else:
        form = UserCreationForm()
    return render(request, 'weblog/signup.html', {'form': form})


# def detail(request,post_id):
#     # try:
#     #    post = Post.objects.get(pk=post_id)
#     # except Post.DoesNotExist:
#         # raise Http404("post does not exist") #next line is shortcut
#     post = get_object_or_404(Post, pk=post_id) 
#     return render(request, 'weblog/detail.html', {'post':post})


# def results(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     return render(request, 'weblog/results.html', {'post': post})


# class IndexView(generic.ListView):
#     template_name = 'weblog/index.html'
#     context_object_name = 'latest_post_list'

#     def get_queryset(self):
#         """Return the last five published posts."""
#         context=dict()
#         context['latest_post_list']=Post.objects.order_by('-pub_date')[:5]
#         context['slider']=slider.objects.all()
#         # context['slider']=post.slider_set.get(pk=request.POST['comment'])
#         print(context)
#         return context['latest_post_list'] 

        

class DetailView(generic.DetailView):
    model = Post
    template_name = 'weblog/detail.html'

class ResultsView(generic.DetailView):
    model = Post
    template_name = 'weblog/results.html'

def vote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    try:
        selected_comment = post.comment_set.get(pk=request.POST['comment'])
    except (KeyError, Comment.DoesNotExist):
        return render(request, 'weblog/detail.html', {
            'post': post,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_comment.votes += 1
        selected_comment.save()
        return HttpResponseRedirect(reverse('weblog:results', args=(post.id,)))