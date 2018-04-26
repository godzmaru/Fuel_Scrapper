# -*- coding: utf-8 -*-

from . import views
from django.conf.urls import url

urlpatterns = [
            url(r'^contact', views.contact, name = 'contact'),  
            url(r'^table', views.fuel_table, name= 'table'),
            url(r'^$', views.index, name = 'index'),
        ]