from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
app_name = 'weblog'

urlpatterns = [
    url(r'^$',views.PostListView.as_view(), name='index'),
    url(r'^posts/create/$',login_required(views.PostCreateView.as_view()), name='create'),
    url(r'^posts/update/$',login_required(views.PostUpdateView.as_view()), name='update'),
    
    url(r'^posts/(?P<slug>[\w-]+)/$',views.PostDetailView.as_view(), name='detail'),
    url(r'^posts/(?P<slug>[\w-]+)/comment/$',login_required(views.CommentCreateView.as_view()), name='comment'),

    url(r'^posts/(?P<slug>[\w-]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^posts/(?P<slug>[\w-]+)/vote/$', views.vote, name='vote'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup2/$', views.signup2, name='signup2'),
    url(r'^signup3/$', views.SignUp3.as_view(), name='signup3'),

    url(r'^searched/$', views.Search.as_view(), name='search'),
    # url(r'^login/$', auth_views.login, {'template_name': 'weblog/login.html'}, name='login'),
    url(r'^login2/$', views.loginn2, name='login2'),
    url(r'^login/$', views.loginn, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'weblog:index'}, name='logout'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
