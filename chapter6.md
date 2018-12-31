#  روز ششم

### <center> ورود با استفاده از ایمیل </center>

 در روز ششم قابلیت ورود با استفاده از ایمیل را به وبلاگ اضافه نمودم



 ```
 urlpatterns = [
    url(r'^signup2/$', views.signup2, name='signup2'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
```

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