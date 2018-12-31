#  روز هشتم

### <center> استفاده از template tags </center>

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

```
{% if posts %}
<ul>
    {% for s in posts %}
        <li>
            {% if s.post_img %}
            <img src="{{ s.post_img.url }}" alt="">
            {% endif %}
            <h5>{{ s.post_title }}</h5>
            <a href="{%  url 'weblog:detail' s.slug %}">{{ s.post_text |truncatechars:20 }}</a>
        </li>
        <hr>
    {% endfor %}
</ul>
{% endif %}
```