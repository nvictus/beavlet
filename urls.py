from django.conf.urls import patterns, include, url
from django.contrib import admin

from apps.nbviewer.views import hello
import apps.nbviewer.urls
import apps.blog.urls

#admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', name='index', view=hello),

    # url(r'^comments/', 
    #     include('django.contrib.comments.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include(apps.blog.urls)),
    url(r'^viewer/', include(apps.nbviewer.urls)),
)
