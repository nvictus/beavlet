from django.conf.urls import patterns, include, url
from django.contrib import admin; admin.autodiscover()

import accounts.urls
import apps.nbviewer.urls
import apps.blog.urls
import apps.dropbox.urls
import apps.dillinger.urls

import views
from apps.nbviewer.views import hello

urlpatterns = patterns('',

    url(r'^$', name='index', view=hello),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include(accounts.urls)),
    url(r'^blog/', include(apps.blog.urls)),
    url(r'^viewer/', include(apps.nbviewer.urls)),
    url(r'^dropbox/', include(apps.dropbox.urls)),
    url(r'^dillinger/', include(apps.dillinger.urls)),

)


# url(r'^comments/', 
#     include('django.contrib.comments.urls')),
