from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',

    url(r'^$', 
        view=views.home),

    url(r'^dropbox-link/$',
        view=views.dropbox_link),

    url(r'^dropbox-auth-finish/$',
        view=views.dropbox_auth_finish),

    url(r'^dropbox-unlink/$', 
        view=views.dropbox_unlink),
)
