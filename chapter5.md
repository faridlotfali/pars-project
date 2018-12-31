#  روز پنجم

### <center> افزودن قابلیت جست و جو </center>

قابلیت جست وجو در پست ها  از مهم ترین قابلیت های وبلاگ است. برای ایجاد این قابلیت باید ویو برای آن ایجاد کرد
 get_queryset  از کلاس سرچ ابتدا متنی دریافت میکند از طریق متود get سپس  به دنبال آن در متن پست ها  و نام نویسنده میگردد و نتیجه را به تمپلیت گفته شده در ابتدا کلاس برمیگرداند تابع 
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

در 

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