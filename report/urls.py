# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from . import views

api_router = routers.DefaultRouter()

urlpatterns = [
    url(r'^list/', views.excel_export, name='list'),
    url(r'^viewreport/$', views.view_report, name='view_report'),
    url(r'^viewreport/xiaoshou/$', views.view_report_xs, name='view_report_xs'),
    url(r'^viewreport/xscharts/$', views.view_report_xs_charts, name='view_report_xs_charts'),
    url(r'^viewreport/xscolumn/$', views.view_report_xs_column, name='view_report_xs_column'),

]
