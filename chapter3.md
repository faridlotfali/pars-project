#  روز سوم

### <center> ایجاد صفحه پست ها </center>
در این روز به ایجاد قسمت اصلی وبلاگ پرداختم و کار را با ایجاد مدل پست آغاز کردم 
مدل پست از فیلد های نویسنده عنوان متن عکس و  تاریخ انتشار تشکیل شده است که در زیر آمده است
نویسنده از یوزر خود جنگو ارت بری میکند 
عنوان و متن از نوع text هستند 
و تاریخ انتشار  نیز از نوع date میباشد

```

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post_title = models.CharField(max_length=300)
    post_text = models.TextField(max_length=3000)
    post_img = models.FileField(upload_to='weblog', blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    pub_date = models.DateTimeField('date published', blank=True, null=True)
    timestamp = models.DateField(auto_now_add = True)
    slug = models.SlugField(null = True,blank = True)
    seen = models.BigIntegerField(default = 0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse('weblog:detail',kwargs = {'slug' : self.slug})    

def p_pre_save_reciever(sender, instance ,*args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

```
تابع pre save که در بالا آمده است هر گاه که یک رکورد ازنوع پست ایجاد شود فراخوانی میشود . 
در این جا این تابع قبل از  ذخیره کردن هر پست به فیلد slug آن مقداردهی میکند.

سپس به نوشتن ویو ها میپردازیم
روشی دیگر برای نوشتن ویو ها روش class based  است 
کلاس زیر برای نمایش لیست کلی از پست ها به کار برده میشود
تابع get_context_data داده هایی که نیاز به نمایش آنها در صفحه تمدلیت است را به آن ارسال میکند.


```

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
```

این کلاس برای نمایش یک تک پست به کار برده میشود و جزییات یک پست را به تمپلیت مد نطر ارسال میکند.
```
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
```       

این کلاس نیز برای ایجاد تغییرات در هر پست به کار برده میشود 


```
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
```