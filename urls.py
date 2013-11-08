from django.conf.urls import patterns, include, url
from django.contrib import admin

import views
import apps.blog.urls

#admin.autodiscover()

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

    # url(r'^comments/', 
    #     include('django.contrib.comments.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include(apps.blog.urls)),
)
