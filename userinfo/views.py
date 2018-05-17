# -*- coding:utf-8 -*-
import urllib
import hgencryp
import json, random, string
from .getToken import WeiXinTokenClass
from django.conf import settings
from urllib import urlencode
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response


# 填入企业号appid, appsecret
WX_SECRET = settings.WX_SECRET
WX_AGENTID = settings.WX_AGENTID
WX_CORPID = settings.WX_CORPID
WX_URL = settings.WX_URL
WX_REDIRECT_URI = settings.WX_REDIRECT_URI
WX_BASE_URL = settings.WX_BASE_URL


authorization_code = ""
access_token = ""


# 是否已经绑定过
def is_bind(userid):
    response = False
    if userid is None or len(userid) == 0:
        return response

    cur=settings.MSCONN.cursor()
    cur.execute('select top 1 1 from [dbo].[wx_usermap] where wxuserid=%s', userid)
    s_data = cur.fetchall()
    cur.close()
    if s_data is not None and len(s_data) != 0:
        response = True

    return response


# 从授权API中检索授权码。
def get_binding_uri(request):
    if request.COOKIES.has_key('userid'):
        userid = request.COOKIES["userid"]
        if is_bind(userid):  # 是否已经绑定过
            return render_to_response('userinfo/dialog.html', {'type': 'tip', 'msg': '已经绑定过帐号'})

    authorization_code_req = {
    "response_type": "code",
    "appid": WX_CORPID,
    "redirect_uri": WX_REDIRECT_URI+'userinfo/getcode/',
    "state": 'binding',
    "scope": (r"snsapi_base" +
              r"snsapi_userinfo")
    }

    uri = WX_BASE_URL + "authorize?%s" % urlencode(authorization_code_req)+'#wechat_redirect'
    return HttpResponseRedirect(uri)


# 从授权API中检索授权码。
def get_discount_uri(request):
    if request.COOKIES.has_key('userid'):
        return classlist(request)
    else:
        authorization_code_req = {
        "response_type": "code",
        "appid": WX_CORPID,
        "redirect_uri": WX_REDIRECT_URI+'userinfo/getcode/',
        "state": 'discount',
        "scope": (r"snsapi_base" +
                  r"snsapi_userinfo")
        }
        uri = WX_BASE_URL + "authorize?%s" % urlencode(authorization_code_req)+'#wechat_redirect'
        return HttpResponseRedirect(uri)


# 取userid
def get_userid(access_token, code):
    userid = ''
    userid_url = '%s/cgi-bin/user/getuserinfo?access_token=%s&code=%s' % (WX_URL,access_token,code)
    response = urllib.urlopen(userid_url)
    result = response.read()
    if 'UserId' in json.loads(result):
        userid = json.loads(result)['UserId']
    return userid


def getcode(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    obj = WeiXinTokenClass()
    access_token = obj.get()
    userid = get_userid(access_token, code)
    if state == 'discount':  # 折扣处理
        cur=settings.MSCONN.cursor()
        cur.execute('select classid,name from [dbo].[st_class] order by classid')
        downlist_tim = dictfetchall(cur)
        response = render_to_response('userinfo/classlist.html', {'classlist': downlist_tim,'userid': userid,})
    elif state == 'binding':  # 绑定处理
        response = render(request, 'userinfo/Binding.html', {'userid': userid,})
    else:
        response = render_to_response('userinfo/dialog.html', {'type': 'error', 'msg': '系统错误'})

    return response


def binding(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    userid = request.POST.get('userid')

    cur = settings.MSCONN.cursor()
    cur.execute('select top 1 id,accountid,password from [dbo].[st_user] where accountid=%s', username)
    s_data = cur.fetchall()
    if s_data is None or len(s_data) == 0:
        return render_to_response('userinfo/dialog.html', {'type': 'error', 'msg': '未找到对应帐号'})
    hguserid = s_data[0][0]
    hgaccountid = s_data[0][1]
    s_password = s_data[0][2]
    if password != hgencryp.UncrypKey(s_password, 'ADDBYHGFFOVER'):
        return render_to_response('userinfo/dialog.html', {'type': 'error', 'msg': '汉高帐号密码错误'})

    cur.execute('select top 1 wxuserid from [dbo].[wx_usermap] where hgaccountid=%s', hgaccountid)
    s_data = cur.fetchall()
    if s_data is not None and len(s_data) != 0:
        s_wxuserid = s_data[0][0]
        if s_wxuserid != userid:
            return render_to_response('userinfo/dialog.html', {'type': 'error', 'msg': '此帐号已经被其它微信绑定'})
        else:
            return render_to_response('userinfo/dialog.html', {'type': 'tip', 'msg': '帐号绑定成功'})
    else:
        cur.execute('INSERT INTO wx_usermap (hguserid, hgaccountid, wxuserid) VALUES( %s,%s,%s)', (hguserid, hgaccountid, userid))
        cur.close()
        settings.MSCONN.commit()
    response = render_to_response('userinfo/dialog.html', {'type':'success', 'msg': '帐号绑定成功'})
    response.set_cookie('userid', userid, 236000*365)

    return response


def makediscount(request):
    ratio = request.POST.get('discount')
    classid = request.POST.get('class')
    userid = request.POST.get('userid')
    mode = 1
    if classid is None or len(classid) == 0:
        mode = 0
    if ratio is None or len(ratio) == 0:
        return render_to_response('userinfo/dialog.html', {'type': 'error', 'msg': '折扣额度不能为空'})
    if userid is None or len(userid) == 0:
        return render_to_response('userinfo/dialog.html', {'type': 'error', 'msg': '请重新绑定帐号'})
    cur=settings.MSCONN.cursor()
    cur.execute('select top 1 hguserid,hgaccountid from [dbo].[wx_usermap] where wxuserid=%s', userid)
    s_data = cur.fetchall()
    if s_data is None or len(s_data) == 0:
        return render_to_response('userinfo/dialog.html', {'type': 'error', 'msg': '请重新绑定帐号'})
    hguserid = s_data[0][0]
    hgaccountid = s_data[0][1]
    discountcode = string.join(random.sample(['1','2','3','4','5','6','7','8','9','1','2','3','4','5','6','7','8','9'], 18)).replace(" ","")
    try:
        cur.execute('INSERT INTO wx_discount (mode,ratio,hguserid,wxuserid,classid,discountcode) VALUES(%d,%d,%s,%s,%s,%s)', (mode,ratio,hguserid,userid,classid,discountcode))
    except:
        return render_to_response('userinfo/dialog.html', {'type': 'error', 'msg': '折扣券生成失败'})
    cur.close()
    settings.MSCONN.commit()
    return HttpResponseRedirect(WX_REDIRECT_URI+'discount/qrcode/'+discountcode)


def classlist(request):
    userid = None
    cur=settings.MSCONN.cursor()
    cur.execute('select classid,name from [dbo].[st_class] order by classid')
    downlist_tim = dictfetchall(cur)
    if request.COOKIES.has_key('userid'):
        userid = request.COOKIES["userid"]
    return render_to_response('userinfo/classlist.html', {'classlist': downlist_tim, 'userid': userid})


def convert_to_json_string_1(data):
    return json.dumps([{'name': i[0], 'value': i[1]} for i in data], indent=4,encoding='UTF-8', ensure_ascii=False)


def test(request):
    #cur=settings.MSCONN.cursor()
    #cur.execute('select classid,name from [dbo].[st_class] order by classid')
    #downlist_tim = ((row[0], row[1]) for row in cur.fetchall())
    #downlist_tim = cur.fetchall()
    #downlist_tim = dictfetchall(cur)
    #a = json.dumps(downlist_tim, encoding='UTF-8', ensure_ascii=False)
    #a = convert_to_json_string_1(downlist_tim)
    #for x in json.loads(a):
    #    print x
    #update/delete/insert,conn.commit()
    #s_date = cur.fetchone()
    #cur.close()

    return hgencryp.UncrypKey('DA022D','ADDBYHGFFOVER')
    #return render_to_response('userinfo/classlist.html', {'classlist': downlist_tim})

# 将返回结果转换成字典
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
