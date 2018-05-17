# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import qrcode
from django.utils.six import BytesIO
from django.shortcuts import render, render_to_response


def special(request):
    return render(request, 'discount/discount.html')

def generate_qrcode(request, data):
    img = qrcode.make(data)        # 传入网站计算出二维码图片字节数据
    buf = BytesIO()                # 创建一个BytesIO临时保存生成图片数据
    img.save(buf)                  # 将图片字节数据放到BytesIO临时保存
    image_stream = buf.getvalue()  # 在BytesIO临时保存拿出数据

    #response = HttpResponse(image_stream, content_type="image/png")
    response = render_to_response('userinfo/dialog.html', {'type': 'error', 'msg': '系统错误'})
    # response = HttpResponse(image_stream, content_type="image/jpg")  #将二维码数据返回到页面
    #response['Last-Modified'] = 'March, 27 Apr 2018 02:05:03 GMT'
    #response['Cache-Control'] = 'max-age=31536000'
    return response