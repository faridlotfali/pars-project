from django.conf.urls import url
from dashboard.views import index
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

app_name = 'dashboard'

urlpatterns = [
    url(r'^$',  index, name='index'),
    # url(r'^$',views.index, name='index'),
]