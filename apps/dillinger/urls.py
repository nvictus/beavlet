from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    #url(r'^(?P<template>[:\w\/ \.-]*\.ejs)$', views.ejs_request)
    url(r'^factory/fetch_markdown$', views.fetch_md),
    url(r'^factory/fetch_html$', views.fetch_html),
    url(r'^factory/fetch_html_direct$', views.fetch_html, {'direct': True}),
    #url(r'$files/md:mdid^', views.download_md),
    #url(r'$files/:html^', views.download_html),

    url(r'^import/dropbox$', views.import_dropbox),
    url(r'^fetch/dropbox$', views.fetch_dropbox_file),
    url(r'^save/dropbox$', views.save_dropbox),
)
