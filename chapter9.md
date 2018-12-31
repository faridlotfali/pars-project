#  روز نهم

### <center> اضافه کردن تنظیمات به سایت  </center>

در روز نهم کاری تصمیم گرفتم تا یک سری تنظیمات کلی به سایت اضافه کنم .
بنابراین به شکل زیر عمل کردم:

```
class SiteSettings(models.Model):
    key_name = models.CharField(max_length=50)    
    key_value = models.TextField(max_length=500)    

    def __str__(self):
        return self.key_name
```

یک مدل کلی به نام SiteSettings   تعریف کردم که دارای فیلد هایkey_name و key_value است که  در اولی نام ویژگی  قرار دارد  و در دومی مقدار آن ویژگی قرار میگرد


```
@register.inclusion_tag('weblog/header.html' , takes_context=True)
def header(context):
    request = context["request"]
    return {'user': request.user }

@register.filter(name='header_settings')
def header_settings(value,args=None):
    header_title = SiteSettings.objects.all().filter(key_name='header').first().key_value
    return header_title

```

سپس به این علت که site setting در اغلب صفحات حضور دارد از تمپلیت تک استفاده میکنیم.
```
from django import template
from ..models import SiteSettings
register = template.Library()


@register.inclusion_tag('weblog/footer.html' , takes_context=True)
def footer(context):
    pass

@register.filter(name='footer_settings')
def footer_settings(value,args = None):
    footer = ''
    if SiteSettings.objects.all().filter(key_name__iexact=value):
        footer= SiteSettings.objects.all().filter(key_name=value)[0].key_value
    return footer
```
    
مدل اسلایدر را نیز به شکل زیر تعریف میکنیم  و از تمپلیت تگ ها برای نمایش آن در صفحات استفاده میکنیم
```
class slider(models.Model):
    image = models.ForeignKey('post', on_delete=models.CASCADE)
```
طرز نمایش اسلایدر در صفخه اصلی به شکل زیر است 
```
{% load static%}
<div id="carouselExampleIndicators" class="carousel slide" data-ride="carousel">
        <ol class="carousel-indicators">
            <li data-target="#carouselExampleIndicators" data-slide-to="0" class="active"></li>
            <li data-target="#carouselExampleIndicators" data-slide-to="1"></li>
            <li data-target="#carouselExampleIndicators" data-slide-to="2"></li>
        </ol>
        <div class="carousel-inner">
            {%  for  data in slider|slice:":3" %}
            <div class="carousel-item {% if forloop.counter0 == 0 %}active{% endif %}">
                <img class="img-fluid" src="{{data.post_img.url}}">
            </div>
            {% endfor%}
        </div>
        <a class="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="sr-only">Previous</span>
        </a>
        <a class="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="sr-only">Next</span>
        </a>
</div>
````
