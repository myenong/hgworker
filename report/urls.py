# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from . import views

api_router = routers.DefaultRouter()

urlpatterns = [
    url(r'^list/', views.excel_export, name='list'),
    url(r'^viewreport/', views.view_report, name='view_report'),

]
