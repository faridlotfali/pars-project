from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic

from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from  weblog.forms import SignUpForm,SignUpForm2
# from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .tokens import account_activation_token
from django.utils.encoding import force_bytes,force_text
# from mysite.core.tokens import account_activation_token
from django.contrib.auth.models import User

from .models import Post,Comment,slider
from django.db.models import Q

#email conf
from django.conf import settings
from django.core.mail import send_mail

def index(request):
    searched = None
    searched_text = request.GET.get("text")
    searched_Author = request.GET.get("Author")
    searched_Author_id = User.objects.filter( username =searched_Author) 
    if searched_Author_id and searched_text : 
        searched = Post.objects.filter(
            Q(post_text__icontains=searched_text) |
            Q(author=searched_Author_id)
            )         
    latest_post_list = Post.objects.order_by('-pub_date')[:5]
    slide = []
    for data in slider.objects.all(): 
        # slide = Post.objects.filter(pk = data) 
        slide.append (list(Post.objects.filter(pk = data.image_id))[0] )
    # slide = Post.objects.filter(pk = 1)
    # output = ', '.join([p.post_text for p in latest_post_list])
    # return HttpResponse(output)
    # template = loader.get_template('weblog/index.html') next code is shortcut
    context = {
        'latest_post_list': latest_post_list,
        'slider' : slide,
        'searched' : searched,
    }
    # return HttpResponse(template.render(context,request)) next code is shortcut
    return  render(request,'weblog/index.html',context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_data')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('weblog:index')
    else:
        form = SignUpForm()
    return render(request, 'weblog/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'weblog/account_activation_sent.html')

def signup2(request):
    if request.method == 'POST':
        form = SignUpForm2(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('weblog/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # user.email_user(subject, message) 
            try:
                send_mail(subject,message, settings.EMAIL_HOST_USER,['farid9lotfali@gmail.com'], fail_silently=False)
            except Exception as e: 
                print(e)
            return redirect('weblog:account_activation_sent')
    else:
        form = SignUpForm2()
    return render(request, 'weblog/signup.html', {'form': form})

# def loginn(request):
    # return render(request, 'weblog/login.html')

def loginn(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print("success")
                # return redirect('weblog:index')
    return render(request ,'weblog/login.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('weblog:index')
    else:
        return render(request, 'weblog/account_activation_invalid.html')




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
    queryset = Post.objects.all()

class ResultsView(generic.DetailView):
    model = Post
    template_name = 'weblog/results.html'

def vote(request, slug):
    post = get_object_or_404(Post, slug=slug)
    try:
        selected_comment = post.comment_set.get(pk=request.POST['comment'])
    except (KeyError, Comment.DoesNotExist):
        return render(request, 'weblog/post_detail.html', {
            'post': post,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_comment.votes += 1
        selected_comment.save()
        return HttpResponseRedirect(reverse('weblog:results', args=(post.slug,)))


