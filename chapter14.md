#  روز چهاردهم

### <center> اتصال django و angular </center>
برای اتصال جنگو و انگولار نیاز به نصب چندین افزونه است که پس نصب آنان نام آنها را در تنظیمات جنگو وارد مینماییم.

```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

پس از نصب موارد گفته شده آدرس هایی را  که اجازه دسترسی به جنگو را داند را وارد میکنیم.
در اینجا آدرس شبکه محلی وارد شده است.
```
ALLOWED_HOSTS = ['982857f4.ngrok.io','localhost']
```