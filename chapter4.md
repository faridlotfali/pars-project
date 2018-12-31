#  روز چهارم

### <center> ایجاد قابلیت کامنت گذاری </center>

قابلیت ایجاد نظر برای هر پست 
```

class Comment(models.Model):
    comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    votes =  models.IntegerField(default=0)

    def __str__(self):
        return self.comment_text

    def get_absolute_url(self):
        return reverse('weblog:detail',kwargs = {'slug' : self.comment.slug})    
```

```

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

```