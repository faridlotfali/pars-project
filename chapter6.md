#  روز ششم

### <center> ورود با استفاده از ایمیل </center>

 در روز ششم قابلیت ورود با استفاده از ایمیل را به وبلاگ اضافه نمودم
در ابتدا تنظیمات مربوط به ایمیلی که میخواهیم با آن لینک ارسال کنیم ار در تنظیمات جنگو وارد میکنیم.
```
# Email Config
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER =  EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```
مقدار دهی به متغیر ها بهتر است در فایل جداگانه انجام شود
```
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = '962comparch' #my gmail password
EMAIL_HOST_USER = 'comp.arch962@gmail.com' #my gmail username
EMAIL_PORT = 587
```
سپس URL  های مناسب با ان را ایجاد میکنیم.
```
 urlpatterns = [
    url(r'^signup2/$', views.signup2, name='signup2'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
```
سپس در ویو ابتدا صحت فرم را چک میکنیم و در صورتی که فرم با  متد post ارسال شده بود اقدام به ارسال ایمیل میکند و در صورتی که فرم خالی بود کاربر را به صفحه signup هدایت میکند.
```
def signup2(request):
    if request.method == 'POST':
        form = SignUpForm2(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('weblog/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # user.email_user(subject, message) 
            try:
                send_mail(subject,message, settings.EMAIL_HOST_USER,['farid9lotfali@gmail.com'], fail_silently=False)
            except Exception as e: 
                print(e)
            return redirect('weblog:account_activation_sent')
    else:
        form = SignUpForm2()
    return render(request, 'weblog/signup.html', {'form': form})
```
بعد از ارسال ایمیل در صورتی که کابر روی لینک کلیک کند تابع زیر به آن جواب میدهد.
<br>
این تابع ابتدا توکن را که در لینک است چک میکند در صورت صحیح بودن چک میکند که اگر یوزر مدنظر وجود  داشت آن را فعال میکند و پس لاگین کردن او ، او ار به صفحه اصلی هدایت میکند.
```
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('weblog:index')
    else:
        return render(request, 'weblog/account_activation_invalid.html')
```