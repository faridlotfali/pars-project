#  روز دوم

### <center> ایجاد صفحه Login و signup </center>

در ابتدا url ها برای این صفحات ست میکنیم


```
urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.loginn, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
]
```
django  به این گونه عمل میکند که هر زمان که یک url  صدا زده شد تابع  متقابل آن را که در قسمت بالا نوشته شده است را فراخوانی میکند.

بعد از نوشتن url ها به نوشتن view ها میپردازیم 

 این تابع ابتدا چک میکند اگر متد ارسالی پست بود صحت فرم را چک میکند در صورت صحیح بودن یوزر مدنظر را  در دیتابیس اضافه میکند.
```
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_data')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('weblog:index')
    else:
        form = SignUpForm()
    return render(request, 'weblog/signup.html', {'form': form})‍
```

تابع لاگین پس از دریافت یوزر و پسورد با استفاده از تابع auth خود django احراز هویت میکند
```
def loginn(request):
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                log.loging(username,request,'login')
                return redirect('weblog:index') 
```
 
 و تابع لاگ اوت نیز به شکل زیر عمل میکند.

```
def logout_view(request):  
    username = request.user     
    logout(request)
    log.loging(username,request,'logout')
    return redirect('weblog:index')
```    

```
{% extends 'weblog/base.html' %}

{% block head_title %}Login || {{ block.super }}{% endblock head_title %}

{% block content %}
  <h2>Log in to My Site</h2>
  <div>
      <form class="form-horizontal" id="login_form1" name="LoginForm1" action="/login/" method="post">
      {% csrf_token %}
      {% if next %}
          <input type="hidden" name="next" value="{{ next }}" />
      {% endif %}
      <div class="control-group">
          <label class="control-label" for="username">Username</label>
          <div class="controls">
              <input type="text" id="username" name="username"  placeholder="Username">
          </div>
      </div>
      <div class="control-group">
          <label class="control-label" for="password">Password</label>
          <div class="controls">
              <input type="password" name="password" id="password" placeholder="Password">
          </div>
      </div>
      <div class="control-group mt-2">
          <div class="controls">
              <button type="submit" class="btn btn-primary">Login</button>
          </div>
      </div>
      </form>
  </div>
{% endblock %}

````
در بالا یک نمونه فرم صفحه لاگین قرار داده شده است که این صفحه در ابتدا از صفحه دیگری ارث بری کرده است 
در داخل  این صفحه یوزر نیم و پسورد از طریق متود post  به ویو مد نظر ارسال میشود.