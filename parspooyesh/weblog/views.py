from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.http import HttpResponse,Http404,HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic import ListView,DetailView,CreateView,UpdateView


from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from  weblog.forms import SignUpForm,SignUpForm2,PostForm,CommentForm
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .tokens import account_activation_token
from django.utils.encoding import force_bytes,force_text
# from mysite.core.tokens import account_activation_token

#paginate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from log_package import log

from django.contrib.auth.models import User
from .models import Post,Comment,slider
from django.db.models import Q

#email conf
from django.conf import settings
from django.core.mail import send_mail

#rest 
from .serializers import * 
from rest_framework import mixins, generics

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response

from django.core.files.storage import FileSystemStorage

from django.views.decorators.csrf import csrf_exempt
import json
from weblog.bot_utils import send_message

@csrf_exempt
def event(request):
    # return JsonResponse({'status':'true' , 'message': 'worked' })
    json_list = json.loads(request.body)
    chat_id = json_list['message']['chat']['id']
    print(chat_id)
    send_message(json_list['message']['text'],chat_id)
    return HttpResponse()
    
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


class SignUp3(APIView):
    throttle_classes = ()
    permission_classes = ()
    """
    Creates the user.
    """
    def get(self, request):
        #do something with 'GET' method
        # return Response("some data")
        serializer = serializers.MyUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

    def post(self, request, format='json'):
        serializer = serializers.MyUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def loginn2(request):
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                log.loging(username,request,'login')
                # return redirect('weblog:index')
        else: 
            return JsonResponse({"success": false ,"error": "username or password not exists"})        
    return redirect('weblog:login')

def logout_view(request):  
    username = request.user     
    logout(request)
    log.loging(username,request,'logout')
    return redirect('weblog:index')

def loginn(request):
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                log.loging(username,request,'login')
                return redirect('weblog:index')         
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

class ResultsView(DetailView):
    model = Post
    template_name = 'weblog/results.html'

class PostListView2(ListView):
    model = Post
    template_name = 'weblog/index.html'
    context_object_name = 'posts'  # Default: object_list
    paginate_by = 6 
    queryset = Post.objects.all()

    def get_context_data(self,*args,**kwargs): 
        context = dict()  
        mostseen = Post.objects.all().order_by('-seen')[:3]
        slide = []
        for data in slider.objects.all(): 
            slide.append (list(Post.objects.filter(pk = data.image_id))[0] )
        context = super(PostListView2, self).get_context_data(*args, **kwargs)
        context['slider']=slide
        context['mostseen']=mostseen
        return context      

class PostListView(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    serializer_class = PostSerializer            
    # model = Post
    template_name = 'weblog/index.html'
    # context_object_name = 'posts'  # Default: object_list
    # paginate_by = 6 
    queryset = Post.objects.all()
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        return self.list(request, *args, **kwargs)
        # return Response({'profiles': queryset})

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_context_data(self,*args,**kwargs): 
        context = dict()  
        mostseen = Post.objects.all().order_by('-seen')[:3]
        slide = []
        for data in slider.objects.all(): 
            slide.append (list(Post.objects.filter(pk = data.image_id))[0] )
        context = super(PostListView, self).get_context_data(*args, **kwargs)
        context['slider']=slide
        context['mostseen']=mostseen
        return context      


class PostDetailView(DetailView):
    def get_queryset(self):
        post = Post.objects.filter(slug =self.kwargs['slug'])[0]
        post.seen += 1
        post.save()
        return Post.objects.filter(slug =self.kwargs['slug'])

class PostCreateView(CreateView):
    template_name = 'weblog/form.html'
    form_class = PostForm
    
    def get_queryset(self):
        return Post.objects.filter(author = self.request.user)
    
    def get_context_data(self,*args,**kwargs): 
        context = super(PostCreateView, self).get_context_data(*args, **kwargs)       
        context['title'] = 'Create Item'
        return context

    def get_form_kwargs(self):
        kwargs = super(PostCreateView,self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        model = form.save(commit=False)
        model.author = self.request.user
        return super(PostCreateView, self).form_valid(form)
       


class PostUpdateView(UpdateView):
    template_name = 'weblog/form.html'
    form_class = PostForm
    def get_queryset(self):
        return Post.objects.filter(author = self.request.user)

    def get_context_data(self,*args,**kwargs): 
        context = super(PostUpdateView, self).get_context_data(*args, **kwargs)       
        context['title'] = 'Update Item'
        return context     

    def get_form_kwargs(self):
        kwargs = super(PostUpdateView,self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        model = form.save(commit=False)
        model.author = self.request.user
        return super(PostUpdateView, self).form_valid(form)

class CommentCreateView(CreateView):
    template_name = 'weblog/form.html'
    form_class = CommentForm
    
    def get_context_data(self,*args,**kwargs): 
        context = super(CommentCreateView, self).get_context_data(*args, **kwargs)       
        context['title'] = 'Create Comment'
        return context  

    def form_valid(self, form):
        model = form.save(commit=False)
        model.comment = Post.objects.filter(slug =self.kwargs['slug'])[0]
        return super(CommentCreateView, self).form_valid(form)

class Search(ListView):
    template_name = 'weblog/searched_result.html'
 
    def get_queryset(self):
        searched_text = self.request.GET.get("text")
        result = None
        searched_Author_id = User.objects.filter( username = self.request.GET.get("Author")) 
        if searched_Author_id:
            result = Post.objects.filter(
                Q(post_text__icontains=searched_text) &
                Q(author=searched_Author_id)
            )
        else :    
            result = Post.objects.filter(
                Q(post_text__icontains=searched_text)
            )
        return result    