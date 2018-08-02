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
    url(r'^signup2/$', views.signup2, name='signup2'),
    url(r'^login/$', auth_views.login, {'template_name': 'weblog/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'weblog:login'}, name='logout'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
