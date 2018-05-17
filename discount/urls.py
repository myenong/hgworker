# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from . import views

api_router = routers.DefaultRouter()

urlpatterns = [
    #url(r'^page/(?P<page>[0-9]+)/$', views.Index.as_view(), name='index'),
    # url(r'^$', views.Index.as_view(), name='index'),
    url(r'^special/', views.special, name='special'),
    url(r'^qrcode/(.+)$', views.generate_qrcode, name='qrcode'),
]
