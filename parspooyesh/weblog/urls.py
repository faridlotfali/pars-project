from django.conf.urls import url
from . import views

app_name = 'weblog'

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<post_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^slider/$', views.slider, name='vote'),
]
