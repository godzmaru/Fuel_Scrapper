# -*- coding: utf-8 -*-

from . import views
from django.conf.urls import url
from django.urls import path

urlpatterns = [
            url(r'^contact', views.contact, name = 'contact'),  
            url(r'^table', views.fuel_table, name= 'table'),
            url(r'^$', views.index, name = 'index'),
            url(r'^mithril', views.mithril_index, name= 'mithril'),
            url(r'^jquery', views.jquery_index, name= 'jquery'),
        ]