from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
	url(r'^$', views.index),
    url(r'^post/(?P<slug>[\w\-]+)$', views.post),
)
