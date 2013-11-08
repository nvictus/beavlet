from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views

urlpatterns = patterns('',

    url(r'^$', 
        name='index',
        view=views.hello),

    url(r'^faq$', 
        name='faq',
        view=views.faq),

    # url(r'^popular$', 
    #     name='popular',
    #     view=views.popular),

    url(r'^create/(?P<value>[\w\/ \.-]*)$', 
        name='create',
        view=views.create),

    url(r'^url/(?P<url>[\w\/ \.-]*)$', 
        name='render_http',
        view=views.fetch_and_render_url, 
        kwargs={'https': False}),

    url(r'^urls/(?P<url>[\w\/ \.-]*)$',
        name='render_https', 
        view=views.fetch_and_render_url,
        kwargs={'https': True}),

    url(r'^(?P<id>[a-f0-9]+)$', 
        name='render_gist',
        view=views.fetch_and_render_gist),
)
