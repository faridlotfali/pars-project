#  روز هفتم

### <center> زیباسازی و رسیدگی به template  </center>


در این روز به زیباسازی و اضافه کردن css به فایل های تمپلیت پرداختم . در فایل های تمپلیت در واقع ظاهر سایت قرار داده میشود . که اضافه کردن css به آن سبب زیباسازی میشود.

برای این کار ابتدا پوشه template را در تنظیمات به django معرفی میکنیم به این شکل :

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

به ظور خودکار خود جنگو به پوشه template در دایرکتوری اصلی  مراجعه میکند. اما اگر نیاز داشته باشیم این دایرکتوری را تغییر دهیم ان را داخل کروشه 'DIRS': [] قرار میدهیم .

برای معرفی کردن فایل های استاتیک از جمله فایل های css و js به صورت زیر عمل میکنیم

<br>

```
STATIC_URL = '/static/'
```

برای  نمونه یکی از فایل های html قرار داده میشود

```
{% extends 'weblog/base.html' %}
{%load static%}
{% block content %}
        <div class="row">
            {% include "weblog/menu.html"%}
        </div> 
    <div class="row">  
    <div class="col-md-9 col-sm-12">
        <div class="row posts">
                {% include "weblog/slider.html"%} 
        {% if object_list %}
        <ul>
        {% for obj in object_list %}
            <li>
                {% if obj.post_img%}
                <img src="{{ obj.post_img.url }}" alt="">
                {%endif%}
                <h3>{{ obj.post_title|truncatechars:20}}</h3>
                <p>{{ obj.created_date }}</p>
                <a class="comment-btn btn btn-info" href="{% url 'weblog:comment' obj.slug %}">Comment</a>
                <a href="{%  url 'weblog:detail' obj.slug %}">{{ obj.post_text|truncatechars:20 }}</a>
            </li>
            <hr>
        {% endfor %}
        </ul>
        {% else %}
        <p>No post are available.</p>
        {% endif %}
        </div>

        {% if is_paginated %}
        <ul class="pagination">
          {% if page_obj.has_previous %}
            <li><a href="?page={{ page_obj.previous_page_number }}">&laquo;</a></li>
          {% else %}
            <li class="disabled"><span>&laquo;</span></li>
          {% endif %}
          {% for i in paginator.page_range %}
            {% if page_obj.number == i %}
              <li class="active"><span>{{ i }} <span class="sr-only">(current)</span></span></li>
            {% else %}
              <li><a href="?page={{ i }}">{{ i }}</a></li>
            {% endif %}
          {% endfor %}
          {% if page_obj.has_next %}
            <li><a href="?page={{ page_obj.next_page_number }}">&raquo;</a></li>
          {% else %}
            <li class="disabled"><span>&raquo;</span></li>
          {% endif %}
        </ul>
      {% endif %}
      
    </div>
    <div class="col-md-3 col-sm-12">
        <div class="row Search-pannel">      
            <form method="GET" action="{% url 'weblog:search' %}" class="index-form" >
                <div class="form-group">
                    <label for="category" class="text-dark">Category</label>
                    <select class="form-control" id="category">
                    <option>All</option>
                    <option>Posts</option>
                    <option>Comments</option>
                    <option>Most voted</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="designer">Author</label>
                    <input type="text" name="Author" class="form-control" id="designer" value="{{ request.GET.Author }}" placeholder="Enter Author name">
                </div>
                <div class="form-group">
                    <label for="contain_word">Contains Words</label>
                    <input type="text" name="text" class="form-control" id="contain_word" value="{{ request.GET.text }}" placeholder="Enter contain words">
                </div>
                <hr>
                <div class="form-group">
                    <button type="submit" class="btn btn-primary">Search</button>
                </div>
            </form>  
        </div>

        <div class="row Search-pannel">
            {% if mostseen %}
            <ul>
                <h2>Most Seen</h2>
            {% for obj in mostseen %}
                <li>
                    <h5>{{ obj.post_title|truncatechars:20}}</h5>
                    <a href="{%  url 'weblog:detail' obj.slug %}">{{ obj.post_text|truncatechars:20 }}</a>
                </li>
                <hr>
            {% endfor %}
            </ul>
            {% else %}
            <p>No post are available.</p>
            {% endif %}
        </div>
    </div>
    </div>
</div>

{% endblock %}


```
‍

 در ابتدا ```{% extends 'weblog/base.html' %}```  امده است که به این معناست که این فایل از base.html ارث بری کرده است.
بعد از فایل های  static لود شده است که همان فایل های css , js هستند
و بع از آن فایل html قرار دارد. قسمت هایی که  بین {} قرار گرفته شده اند برای داینامیک کردن فایل html  به کار میرود.