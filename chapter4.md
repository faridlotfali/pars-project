#  روز چهارم

### <center> ایجاد قابلیت کامنت گذاری </center>

در این روز تصمیم گرفتم که قابلیت کامنت گذاری را برای هر پست به صورت جداگانه ایجاد  کنم.
در ابتدا مدل کامنت را به شکل زیر ایجاد کردم. این مدل شامل متن کامنت تعداد رای ها و یک forgein key به پست است که نشان میدهد هر کامنت به یک پست نظیر شده است.
تابع```  __str__``` نشان میدهد که در صورت فراخوانی یک شی از این کلاس چه چیزی نمایش داده شود.
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


سپس به ایجاد ویو برای این قسمت پرداختم 
ویو نوشته شده در زیر به روش class based  است . هر زمان فرم کامنت ارسال شود تابع form_valid فراخوانی میشود.
و هر زمان که نیاز به دریافت کامنت ها از متد get باشد تابع  get_context_data فراخوانی میشود.
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

نمونه فرم که در صفحه هر پست قرار داده میشود و با تایید کردن به ویو مد نظر ارسال میشود
```
        <div class="row col-12">
            <form action="{% url 'weblog:vote' post.slug %}" method="post">   
            {% csrf_token %}
            {% for comment in post.comment_set.all %}
                <input type="radio" name="comment" id="comment{{ forloop.counter }}" value="{{ comment.id }}" />
                <label for="comment{{ forloop.counter }}">{{ comment.comment_text }}</label><br />
            {% endfor %}
            <button type="submit" class="btn btn-primary">vote</button>
            </form>
        </div>
```    
و url آن که کامنت به ارسال میشود به شکل زیر است .
برای ارسال کامنت نیاز به لاگین شدن است.

```
urlpatterns = [
    url(r'^posts/(?P<slug>[\w-]+)/comment/$',login_required(views.CommentCreateView.as_view()), name='comment'),
]
```