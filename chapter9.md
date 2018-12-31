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
    
```
class slider(models.Model):
    image = models.ForeignKey('post', on_delete=models.CASCADE)
```
