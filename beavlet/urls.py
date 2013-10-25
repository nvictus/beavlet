from django.conf.urls import patterns, include, url
from django.contrib import admin

import beavlet.views

#admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 
        name='index',
        view=beavlet.views.hello),

    url(r'^faq$', 
        name='faq',
        view=beavlet.views.faq),

    url(r'^popular$', 
        name='popular',
        view=beavlet.views.popular),

    url(r'^create/(?P<value>[\w\/ \.-]*)$', 
        name='create',
        view=beavlet.views.create),

    url(r'^url/(?P<url>[\w\/ \.-]*)$', 
        name='render_http',
        view=beavlet.views.fetch_and_render_url, 
        kwargs={'https': False}),

    url(r'^urls/(?P<url>[\w\/ \.-]*)$',
        name='render_https', 
        view=beavlet.views.fetch_and_render_url,
        kwargs={'https': True}),

    url(r'^(?P<id>[a-f0-9]+)$', 
        name='render_gist',
        view=beavlet.views.fetch_and_render_gist),
    #url(r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),
    #url(r'^admin/', include(admin.site.urls)),
)
