#  روز دهم

### <center> ورود با ajax </center>

در روز  دهم قابلیت ورود با استفاده ajax را به وبلاگ خود اضافه کردم .
ajax قابلیتی است که میتوان داده ها را بدون رفرش شدن صفحه ارسال کرد .

<br>
 در ابتدا url مربوطه را اضافه میکنیم
```

urlpatterns = [
    url(r'^login2/$', views.loginn2, name='login2'),
    url(r'^logout/$', views.logout_view, name='logout'),
]

```
سپس در فایل Html کد زیر را در آخر صفحه اضافه میکنیم.
کد زیر یوزر و پسورد را با متد پست به /login2/ ارسال میکند و درصورت صحیح بودن پیغام hi username را نمایش میدهد
```
<script>
    
        $(document).on('submit','#login_form', function(e){
          e.preventDefault();
          var user = $('#username').val();
          $.ajax({
            type:'POST',
            url : '/login2/',
            data:{
              username:$('#username').val(),
              password:$('#password').val(),
              csrfmiddlewaretoken: $('input[name = csrfmiddlewaretoken ]').val(),
            },
            success: function(){
                $('#Hiusername').text(`hi ${user}`);
                $('.login-text').text(' ');
                $('#login').modal('toggle');
                $('#login').removeClass('in');
                $('#login').attr("aria-hidden","true");
                $('#login').css("display", "none");
                $('.modal-backdrop').remove();
                $('body').removeClass('modal-open');
                setTimeout(function(){},2000);
            },
            error: function(error){
               alert("username or password doesnt exist");
               }
          });
  
        });
      </script>
```
در کد زیر در صورت اینکه متد ارسالی پست بود یوزر را authenticate میکند و سپس آن را لاگین میکند. در غیر این صورت ارور برمیگرداند.
```
def loginn2(request):
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                log.loging(username,request,'login')
                # return redirect('weblog:index')
        else: 
            return JsonResponse({"success": false ,"error": "username or password not exists"})        
    return redirect('weblog:login')
```