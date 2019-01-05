#  روز یازدهم

### <center> اضافه کردن celery </center>
برای ایجاد تسک های مشخص در زمان های مشخص و شرایط معین از celery استفاده میکنیم.

بطور خلاصه celery چطوری کار می‌کنه؟

جنگو به یک message broker (اینجا ما از RabbitMQ استفاده کردیم ) یک پیامی (تسکی) را می‌فرسته. message broker هم این پیام را به یکی از ورکرهایی که مختص این کاره ارجاع می‌دهد. در مرحله‌ی آخر هم ورکر مربوطه کار را در پشت پرده انجام می‌دهد.


در ابتدا RabbitMQ را نصب میکنیم.سپس تنظیمات زیر را به جنگو اضافه میکنیم.

```
CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'
CELERY_RESULT_BACKEND = 'amqp://guest:guest@localhost//'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
```

بعد از وارد کردن تنظیمات تسک های مد نظر خود ار وارد میکنیم.
در نمونه کد زیر سه تسک مختلف را میخواهیم در زمان های مختلف انجام دهیم.
این تسک ها عبارتند از تابع های ```multiply_two_numbers``` و ```tasks.add```


```
#install rabiamq apt-get install -y erlang  apt-get install rabbitmq-server

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parspooyesh.settings')

app = Celery('parspooyesh')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request))

from celery.schedules import crontab
app.conf.beat_schedule = {
    'add-every-minute-contrab': {
        'task': 'multiply_two_numbers',
        'schedule': crontab(),
        'args': (16, 16),
    },
    'add-every-5-seconds': {
        'task': 'multiply_two_numbers',
        'schedule': 5.0,
        'args': (16, 16)
    },
    # 'add-every-30-seconds': {
    #     'task': 'tasks.add',
    #     'schedule': 30.0,
    #     'args': (16, 16)
    # },
}  
```
جزییات تابع های گفته شده در زیر آمده است که یک تابع جمع و یک تابع ضرب نوشته شده است.
```
from __future__ import absolute_import, unicode_literals
import random
from celery.decorators import task

@task(name="sum_two_numbers")
def add(x, y):
    return x + y

@task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * random.randint(3, 100))
    return total

@task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)
```