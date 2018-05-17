# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import HttpResponse
from django.conf import settings
from StringIO import StringIO
from xlwt import *
import os
from django.shortcuts import render, render_to_response
from django import forms

from django.shortcuts import render

# Create your views here.

def view_report_xs_column(request):
    cur = settings.MSCONN.cursor()
    cur.execute('select e.name as comname,cast(round(sum(a.c_number * a.c_price)/10000,2)as  numeric(12,2)) as money '
                'from retail_list_dtl a '
                'left join retail_list b on a.c_retailcode=b.c_retailcode '
                'left join st_company  e on b.belong_comid = e.id '
                'group by e.name')
    list_tim = dictfetchall(cur)
    return render_to_response('report/reportview_xs_column.html', {'xslist': list_tim})

def view_report_xs_charts(request):
    cur = settings.MSCONN.cursor()
    cur.execute('select e.name as comname,cast(round(sum(a.c_number * a.c_price),2)as  numeric(12,2)) as money '
                'from retail_list_dtl a '
                'left join retail_list b on a.c_retailcode=b.c_retailcode '
                'left join st_company  e on b.belong_comid = e.id '
                'group by e.name')
    list_tim = dictfetchall(cur)
    return render_to_response('report/reportview_xs_charts.html', {'xslist': list_tim})


def view_report_xs(request):
    cur = settings.MSCONN.cursor()
    cur.execute('select b.c_selldeptname as deptname,cast(round(sum(a.c_number * a.c_price),2)as  numeric(12,2)) as money  ' +
                'from retail_list_dtl a '
                'left join retail_list b on a.c_retailcode=b.c_retailcode '
                'group by b.c_selldeptname')
    list_tim = dictfetchall(cur)
    return render_to_response('report/reportview_xs.html', {'xslist': list_tim})


def view_report(request):
    cur=settings.MSCONN.cursor()
    cur.execute('select classid,name from [dbo].[st_class] order by classid')
    list_tim = dictfetchall(cur)
    return render_to_response('report/reportview.html', {'classlist': list_tim})


# 将返回结果转换成字典
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def excel_export(request):
    cur=settings.MSCONN.cursor()
    cur.execute('select * from [dbo].[wx_usermap]')
    s_data = cur.fetchall()
    list_obj = s_data
    if list_obj:
        # 创建工作薄
        ws = Workbook(encoding='utf-8')
        w = ws.add_sheet(u"数据报表第一页")
        w.write(0, 0, "id")
        w.write(0, 1, u"用户名")
        w.write(0, 2, u"发布时间")
        w.write(0, 3, u"内容")
        w.write(0, 4, u"来源")
        # 写入数据
        excel_row = 1
        for obj in list_obj:
            data_id = obj[1]
            data_user = obj[1]
            data_time = obj[2]
            data_content = obj[3]
            dada_source = obj[4]
            w.write(excel_row, 0, data_id)
            w.write(excel_row, 1, data_user)
            w.write(excel_row, 2, data_time)
            w.write(excel_row, 3, data_content)
            w.write(excel_row, 4, dada_source)
            excel_row += 1

        file = os.path.join(settings.MEDIA_ROOT, "test.xls")
        if os.path.exists(file):
            os.remove(file)
        ws.save(file)

        sio = StringIO()
        ws.save(sio)
        sio.seek(0)
        response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename='+file
        response.write(sio.getvalue())
        return response