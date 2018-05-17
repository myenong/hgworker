# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from . import views

api_router = routers.DefaultRouter()

urlpatterns = [
    url(r'^getcode/', views.getcode, name='getcode'),
    url(r'^getdiscounturi/', views.get_discount_uri, name='getdiscounturi'),
    url(r'^getbindinguri/', views.get_binding_uri, name='getbindinguri'),
    url(r'^binding/', views.binding, name='binding'),
    url(r'^classlist/', views.classlist, name='classlist'),
    url(r'^discount/', views.makediscount, name='discount'),
    url(r'^test/', views.test, name='test'),

]
