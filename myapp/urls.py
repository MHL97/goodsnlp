#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'goodscomments.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^welcome/', views.welcome),
    url(r'^search/', views.search, name='search'),
    url(r'^analysis/', views.analysis, name='analysis'),
    # url(r'^visual/', views.visual, name='visual'),
]