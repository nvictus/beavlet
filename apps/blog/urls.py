from django.conf.urls import patterns, include, url
from apps.blog import views

urlpatterns = patterns('',
	url(r'^$', views.index),
    url(r'^post/(?P<slug>[\w\-]+)$', views.post),
    url(r'^register/$', views.register_page),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', views.logout_page),
)
