# -*- coding: utf-8 -*-

from . import views
from django.conf.urls import url

urlpatterns = [
            url(r'^contact', views.contact, name = 'contact'),  
            url(r'^table', views.fuel_table, name= 'table'),
            url(r'^$', views.index, name = 'index'),
            url(r'^mithril/$', views.mithril_index, name= 'mithril'),
            url(r'^mithril/by/product', views.mithril_json, name= 'mithril_data'),
            url(r'^jquery', views.jquery_index, name= 'jquery'),
        ]