#  روز سیزدهم

### <center> استفاده از rest framework </center>

رست فریمورک قابلیتی است که امکان ایجاد api را در جنگو برای ما فراهم میکند.

پس نصب آن با دستور 
```
pip install django-restframework
```
تنظیمات زیر را در جنگو وارد مینماییم

fields مشخص میکند که چه فیلد هایی باید ارسال شوند 
model  مشخص میکند که از چه جدولی از دیتابیس خوانده شود
```
from rest_framework import serializers
from django.contrib.auth.models import User 
from .models  import *

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('author', 'post_title', 'post_text')

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token'
        ]
```
تابع زیر یک ویو بر اساس json میباشد 
که با استفاده از تابع HttpResponse مقادیر خواسته شده را بر میگرداند

```
def event(request):
    # return JsonResponse({'status':'true' , 'message': 'worked' })
    json_list = json.loads(request.body)
    chat_id = json_list['message']['chat']['id']
    print(chat_id)
    send_message(json_list['message']['text'],chat_id)
    return HttpResponse()
```    