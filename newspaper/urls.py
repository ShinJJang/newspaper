from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'newspaper.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/',         include(admin.site.urls)),
    url(r'^$',              'news.views.index', name='index'),
    url(r'^login/$',        'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^signup/$',       'news.views.signup', name='signup'),
    url(r'^signup/submit$',       'news.views.signup_submit', name='signup_submit'),
    # logout
    # newest
    # submit thread
    # read thread
    # edit profile
)
