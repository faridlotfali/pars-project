#  روز پنجم

### <center> افزودن قابلیت جست و جو </center>

قابلیت جست وجو در پست ها  از مهم ترین قابلیت های وبلاگ است. برای ایجاد این قابلیت باید ویو برای آن ایجاد کرد
 get_queryset  از کلاس سرچ ابتدا متنی دریافت میکند از طریق متود get سپس  به دنبال آن در متن پست ها  و نام نویسنده میگردد و نتیجه را به تمپلیت گفته شده در ابتدا کلاس برمیگرداند  
```
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
```

در کد زیر ابتدا از ```base.html``` ارث بری کرده ایم و سپس نتیجه جست جودر پیت ها برگردانیم که این نتایج در یک آرایه قرار دارند و با استفاده از یک حلقه هر کدام را نمایش دادیم در آخر نیز یک لینک به هر پست وجود دارد.

```
{% extends 'weblog/base.html' %}
{% block content %}
<div class="default-div" style="height: 500px; width: 100%;">
<h1>Search Result:</h1>
{% if object_list %}
<ul>
    {% for s in object_list %}
        <li>
            <img src="{{ post.post_img.url }}" alt="">
            <h3>{{ s.post_title }}</h3>
            <a href="{%  url 'weblog:detail' s.slug %}">{{ s.post_text }}</a>
        </li>
        <hr>
    {% endfor %}
</ul>
{% endif %}
</div>
{% endblock %}
```

لینک به صفحه  detail  هر محصول میرود که در کد زیر به نمایش در آمده است در این  صفحه مشخصات هر پست از جمله عکس  عنوان و متن و به علاوه کامنت های آن موجود است.

```
{% extends 'weblog/base.html' %}

{% block head_title %}detail || {{ block.super }}{% endblock head_title %}

{% block content %} 
<div class="results container">
    <div class="row">
        <div class="col-12">
            {% if object.post_img%}  
            <img src="{{ object.post_img.url }}" alt=""  style="height: 35em;">
            {% endif %}
        </div>   
        <div class="col-12">
            <h1>{{object.post_title}}</h1>
            <h3>{{object.post_text}}</h3>
        </div>
    </div>      
        {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
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
    </div>
</div>
{% endblock %}
```