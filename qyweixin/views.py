# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse

from django.shortcuts import render
import urllib
import json
from django.conf import settings
from django.core.cache import cache

corpid = settings.WX_CORPID
corpsecret = settings.WX_SECRET
url = settings.WX_URL
msg = '企业微信订阅报表'

# Create your views here.

# --------------------------------
# 获取企业微信token
# --------------------------------


def get_token(url, corpid, corpsecret):
    token_url = '%s/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (url, corpid, corpsecret)
    token = json.loads(urllib.urlopen(token_url).read().decode())['access_token']
    return token

# --------------------------------
# 构建告警信息json
# --------------------------------
def messages(msg):
    values = {
        "touser": '@all',
        "msgtype": 'text',
        "agentid": 1000004,
        "text": {'content': msg},
        "safe": 0
        }
    # msges=(bytes(json.dumps(values), 'utf-8'))
    msges=(json.dumps(values))
    return msges

#--------------------------------
# 发送告警信息
#--------------------------------
def send_message(url,token, data):
        send_url = '%s/cgi-bin/message/send?access_token=%s' % (url,token)
        respone = urllib.urlopen(url=send_url, data=data).read()
        x = json.loads(respone.decode())['errcode']
        if x == 0:
            s = 'Succesfully'
            # print ('Succesfully')
        elif x == 42001:
            settings.WX_AUTH_ACCESS_TOKEN = get_token(url, corpid, corpsecret)
            send_url = '%s/cgi-bin/message/send?access_token=%s' % (url,token)
            respone = urllib.urlopen(url=send_url, data=data).read()
            x = json.loads(respone.decode())['errcode']
            s = 'Succesfully'
        else:
            s = 'Failed'
            # print ('Failed')
        return s

# #############函数结束########################


def test(request):
    # 函数调用
    settings.WX_AUTH_ACCESS_TOKEN = get_token(url, corpid, corpsecret)
    msg_data = messages(msg)
    s = send_message(url, settings.WX_AUTH_ACCESS_TOKEN, msg_data)
    return HttpResponse(json.dumps(s, encoding='UTF-8', ensure_ascii=False))