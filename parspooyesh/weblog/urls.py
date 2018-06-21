from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'weblog'

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<post_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.login, {'template_name': 'weblog/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'weblog:login'}, name='logout'),
]
