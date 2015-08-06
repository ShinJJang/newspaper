from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from news.api import CommentResource, UserResource, ThreadResource

v1_api = Api(api_name='v1')
v1_api.register(CommentResource())
v1_api.register(UserResource())
v1_api.register(ThreadResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'newspaper.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/',                 include(admin.site.urls)),
    url(r'^$',                      'news.views.index', name='index'),
    url(r'^login/$',                'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^signup/$',               'news.views.signup', name='signup'),
    url(r'^signup/submit/$',        'news.views.signup_submit', name='signup_submit'),
    url(r'^logout/$',               'news.views.user_logout', name='user_logout'),
    url(r'^thread/new/$',           'news.views.new_thread', name='new_thread'),
    url(r'^thread/submit/$',        'news.views.submit_thread', name='submit_thread'),
    url(r'^thread/(?P<thread_id>\d+)/$', 'news.views.read_thread', name='read_thread'),
    url(r'^thread/(?P<thread_id>\d+)/vote/$', 'news.views.vote', name='vote'),
    url(r'^thread/(?P<thread_id>\d+)/comment/$', 'news.views.get_comments', name='get_comments'),
    (r'^api/', include(v1_api.urls)),
    # edit profile
    # submit comment
    # about
)
