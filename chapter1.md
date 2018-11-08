

#  روز اول

### <center> مطالعه جنگو </center>
<p>
روز اول را با مطالعه داکیومنت های جنگو شروع کردم. جنگو یک فریمورک برای برنامه نویسی وب است که از زبان  پایتون استفاده میکند.این فریمورک یک فریم ورک و چارچوب جدید و برجسته وب است، اما معنی دقیق یک چارچوب یا فریم ورک چیست؟
<br>
</p>
<p>
برای جواب دادن به سوال بالا، در ابتدا طرح یک برنامه وب نوشته شده در پایتون را بدون استفاده از فریمورک یا چارچوب بررسی می کنیم . 
یکی از آسان ترین روش های ساخت یک برنامه وب پایتون، استفاده از CGI می باشد، که در حدود سال های 1998 محبوب بود. تنها کافی است یک اسکریپت پایتون که خروجی HTML تولید می کند نوشته، سپس اسکریپت را با پسوند ".cgi" درون وب سرور ذخیره کنیم و در آخر نیز صفحه را درون مرورگر خود مشاهده کنیم.
</p>

```
#!/usr/bin/env python

import MySQLdb

print "Content-Type: text/html\n"
print "<html><head><title>Books</title></head>"
print "<body>"
print "<h1>Books</h1>"
print "<ul>"

connection = MySQLdb.connect(user='me', passwd='letmein', db='my_db')
cursor = connection.cursor()
cursor.execute("SELECT name FROM books ORDER BY pub_date DESC LIMIT 10")

for row in cursor.fetchall():
    print "<li>%s</li>" % row[0]

print "</ul>"
print "</body></html>"

connection.close()

```
اما با وجود تمام این سادگی ها، در استفاده کلی از روش بالا ممکن است با مسائل و مشکلاتی روبه رو شویم. مطمئنا کد مربوط به اتصال به دیتابیس نیازی نیست در CGI اسکریپت ها به صورت منحصر به فرد تکرار شود. یک چارچوب وب درست مانند یک زیرساخت برای برنامه های ماست، به طوری که می توانیم روی تمیز برنامه نوشتن یا کد قابل اصلاح بدون دوباره نویسی تمرکز کنیم، خلاصه اینکه جنگو تمام وظایف ذکر شده را انجام می دهد.

<br>

###  الگوی طراحی MVC
بیایید یک مثال که تفاوت بین روش قبلی و روش با استفاده از فریم ورک یا چارچوب وب را نشان می دهد را مورد بررسی قرار دهیم. در اینجا نحوه نوشتن کد قبلی CGI را با استفاده از جنگو نشان داده شده است. اولین چیزی که باید توجه کنید این است که ما عملیات انجام شده در کد قبلی را در سه فایل پایتون models.py، views.py، urls.py و یک فایل
latest_books.html از هم جدا کرده ایم:

```
# models.py (the database tables)

from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=50)
    pub_date = models.DateField()


# views.py (the business logic)

from django.shortcuts import render_to_response
from models import Book

def latest_books(request):
    book_list = Book.objects.order_by('-pub_date')[:10]
    return render_to_response('latest_books.html', {'book_list': book_list})


# urls.py (the URL configuration)

from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^latest/$', views.latest_books),
)


# latest_books.html (the template)

<html><head><title>Books</title></head>
<body>
<h1>Books</h1>
<ul><ul/>
{% for book in book_list %}
<li>id="19"<li/>
{{ book.name }}
</li>

{% endfor %}
</ul>
</body></html>
```

1. فایل<b>models.py</b> حاوی یک توضیح از جدول دیتابیس می باشد که بصورت کلاس پایتون نمایش داده شده است. این کلاس یک model نامیده می شود. با استفاده از آن شما می توانید رکوردهای درون دیتابیس را با استفاده از کد ساده پایتون ساخته، بازیابی، به روز سازی و حذف کنید.

2. فایل<b>views.py</b> حاوی منطق های برنامه نویسی برای صفحه می باشد. تابع latest_books() با نام view شناخته می شود.

3. فایل<b>urls.py</b> نسبت به url داده شده view مورد نظر را تعیین می کند. در مثال فوق /latest/ با تابع latest_book مرتبط خواهد شد. به زبان ساده تر، اگر دامنه شما example.com است، هر بازدیدی از آدرس example.com/latest تابع latest_book را فراخوانی خواهد کرد.

4. فایل <b>latest_books.html</b> 
 یک قالب HTML  است که طرح صفحه در آن قرار می گیرد.
این قالب از یک زبان template با جملات منطقی پایه استفاده می کند.

<br>

قسمت های فوق یک الگو را دنبال می کنند که Model-View-Controller یا (MVC) نامیده می شود. به عبارت ساده MVC یک روش برای توسعه دادن نرم افزار است به طوری که کد برای تعریف کردن و دسترسی داشتن داده (the model) از منطق (the controller) جدا شده و آن نیز از رابط کاربر (the view) جدا می باشد. (ما در مورد MVC در آموزش مدل جنگو به طور مفصل بحث خواهیم کرد.)


مزیت کلیدی روش MVC این است که اجزا نسبت به یکدیگر به اصطلاح loosely coupled هستند. بدین معنا که هر قسمت مجزا از برنامه تحت وب جنگو هدف خاص خود را دارد و می تواند بدون تاثیربر روی دیگر قسمت ها به طور مستقل تغییر کند. به عنوان مثال، یک توسعه دهنده می تواند مسیر یک بخش داده شده از برنامه را بدون تاثیر بر روی اصل برنامه تغییر دهد. یک طراح می تواند صفحه HTML را بدون کار کردن با کد پایتون تغییر داده و تحویل دهد. یک مدیر دیتابیس می تواند جداول درون دیتابیس را تغییر نام داده و هر تغییری را درون یک قسمت خاص بدهد.


در این کتاب، هر بخش از MVC درون فصل خود بحث شده است. آموزش view و urlconf جنگو views را پوشش می دهد، آموزش template جنگو templates را و آموزش مدل جنگو نیز models را پوشش می دهد.