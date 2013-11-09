from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

import views

from apps.nbviewer.views import hello
import apps.nbviewer.urls
import apps.blog.urls
import apps.dropbox.urls

urlpatterns = patterns('',

    url(r'^$', name='index', view=hello),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^blog/', include(apps.blog.urls)),
    url(r'^viewer/', include(apps.nbviewer.urls)),
    url(r'^dropbox/', include(apps.dropbox.urls)),

    url(r'^accounts/login/$', views.login),
    url(r'^accounts/auth/$', views.auth_view),
    url(r'^accounts/logout/$', views.logout),
    url(r'^accounts/loggedin/$', views.loggedin),
    url(r'^accounts/invalid/$', views.invalid_login),
    url(r'^accounts/register/$', views.register_user),
    url(r'^accounts/register_success/$', views.register_success),
)


# url(r'^comments/', 
#     include('django.contrib.comments.urls')),
