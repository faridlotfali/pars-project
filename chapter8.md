#  روز هشتم

### <center> استفاده از template tags </center>

تمپلیت تگ ها یکی از زیباترین قابلیت های جنگو هستند .با استفاده از آن ها قادر خواهیم بود که یک سری کارهایی را که اکثر صفحات تکرار میشوند را در قالب یک تمپلیت کلی تعریف کنیم 

<br>
در وبلاگ ما میخواهیم آخرین پست ها را در تمام صفحات داشته باشیم بنابراین آن را در قالب یک تمپلیت تگ تعریف میکنیم
```
from django import template
from ..models import Post
register = template.Library()


# @register.inclusion_tag('weblog/header.html' , takes_context=True)
@register.inclusion_tag('weblog/last_posts.html')
def last_post():
    posts = Post.objects.all()[:3]
    return {'posts': posts}

```
برای لود کردن تمپلیت در صفحات از دستور ```load last_posts_tags``` استفاده میکنیم .
```
{% load last_posts_tags %}
  <div class="row posts">
    <div class="col-md-5 last_posts">
        <h1>Last Posts</h1>
  {% last_post %}
    </div>

    <div class="col-md-5 last_posts">
        <h1>My Posts</h1>
        {% if user_post_list %}
        <ul>
            {% for s in user_post_list %}
                <li>
                  {% if s.post_img%}
                    <img src="{{ s.post_img.url }}" alt="">
                    {% endif%}
                    <h5>{{ s.post_title }}</h5>
                    <a href="{%  url 'weblog:detail' s.slug %}">
                    {{ s.post_text |truncatechars:20 }}
                    </a>
                </li>
                <hr>
            {% endfor %}
        </ul>
        {% endif %}
    </div>
  </div>
</div>
```
بعد از لود کردن آن با استفاده از حلقه مقادیر آخرین پست را نمایش میدهیم.
تابع truncatechars که در بالا آمده است حداکثر تعداد کاراکتر که بعد اژ آن آمده است را نمایش میدهد.
<br>
در روز های دیگر از همین روش برای قسمت هایی که در اکثر صفحات هستند استفاده شده است. 