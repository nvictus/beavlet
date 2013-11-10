from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    url(r'^login/$', views.login),
    url(r'^auth/$', views.auth_view),
    url(r'^logout/$', views.logout),
    url(r'^loggedin/$', views.loggedin),
    url(r'^invalid/$', views.invalid_login),
    url(r'^register/$', views.register_user),
    url(r'^register_success/$', views.register_success),
)
