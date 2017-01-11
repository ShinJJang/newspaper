from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from news import views as news_views
from tastypie.api import Api
from news.api import CommentResource, UserResource, ThreadResource

v1_api = Api(api_name='v1')
v1_api.register(CommentResource())
v1_api.register(UserResource())
v1_api.register(ThreadResource())

urlpatterns = [
    # Examples:
    # url(r'^$', 'newspaper.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/',                 include(admin.site.urls)),
    url(r'^$',                      news_views.index, name='index'),
    url(r'^login/$',                auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^signup/$',               news_views.signup, name='signup'),
    url(r'^signup/submit/$',        news_views.signup_submit, name='signup_submit'),
    url(r'^logout/$',               news_views.user_logout, name='user_logout'),
    url(r'^thread/new/$',           news_views.new_thread, name='new_thread'),
    url(r'^thread/submit/$',        news_views.submit_thread, name='submit_thread'),
    url(r'^thread/(?P<thread_id>\d+)/$', news_views.read_thread, name='read_thread'),
    url(r'^thread/(?P<thread_id>\d+)/vote/$', news_views.vote, name='vote'),
    url(r'^api/', include(v1_api.urls)),
    # edit profile
    # about
]
