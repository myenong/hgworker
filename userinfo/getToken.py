# -*- coding: utf8 -*-

import sys
import urllib
import urllib2
import json
import datetime
from .models import weixin_token, weixin_account
from django.conf import settings


def debug(msg, code=None):
    if settings.enable_debug:
        if code is None:
            print "message: %s" % msg
        else:
            print "message: %s, code: %s " % (msg, code)


weixin_qy_CorpID = settings.WX_CORPID
weixin_qy_Secret = settings.WX_SECRET


def sqlite3_set_credential(corpid, secret):
    weixin_account.objects.create(
            name = 'odbp',
            corpid = corpid,
            secret = secret,
            current = 1
            )


def sqlite3_set_token(access_token, expires_in, expires_on, is_expired):
    weixin_token.objects.create(
            access_token = access_token,
            expires_in = expires_in,
            expires_on = expires_on,
            is_expired  =is_expired
            )


def sqlite3_get_credential():
    credential = weixin_account.objects.filter(current=1).values_list('corpid', 'secret')
    return credential


def sqlite3_get_token():
    try:
        credential = weixin_token.objects.filter(is_expired=1).values_list('access_token', 'expires_on')
        result = credential
    except:
        info = sys.exc_info()
        print info[0], ":", info[1]
    else:
        if result is not None and result.count() != 0:
            return result
        else:
            return None


def sqlite3_update_token(access_token, expires_on):
    weixin_token.objects.all().update(access_token=access_token, expires_on=expires_on)

class WeiXinTokenClass(object):
    def __init__(self):
        self.__corpid = None
        self.__corpsecret = None
        self.__use_persistence = True

        self.__access_token = None
        self.__expires_in = None
        self.__expires_on = None
        self.__is_expired = None

        if self.__use_persistence:
            self.__corpid = sqlite3_get_credential()[0][0]
            self.__corpsecret = sqlite3_get_credential()[0][1]
        else:
            self.__corpid = weixin_qy_CorpID
            self.__corpsecret = weixin_qy_Secret

    def __get_token_from_weixin_qy_api(self):
        parameters = {
            "corpid": self.__corpid,
            "corpsecret": self.__corpsecret
        }
        url_parameters = urllib.urlencode(parameters)
        token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?"
        url = token_url + url_parameters
        response = urllib2.urlopen(url)
        result = response.read()
        token_json = json.loads(result)
        if token_json['access_token'] is not None:
            get_time_now = datetime.datetime.now()
            # TODO(Guodong Ding) token will expired ahead of time or not expired after the time
            expire_time = get_time_now + datetime.timedelta(seconds=token_json['expires_in'])
            token_json['expires_on'] = str(expire_time)
            self.__access_token = token_json['access_token']
            self.__expires_in = token_json['expires_in']
            self.__expires_on = token_json['expires_on']
            self.__is_expired = 1

            try:
                token_result_set = sqlite3_get_token()
            except:
                token_result_set = None
            if token_result_set is None or token_result_set.count() == 0:
                sqlite3_set_token(self.__access_token, self.__expires_in, self.__expires_on, self.__is_expired)
            else:
                if self.__is_token_expired() is True:
                    sqlite3_update_token(self.__access_token, self.__expires_on)
                else:
                    debug("pass")
                    return
        else:
            if token_json['errcode'] is not None:
                print "errcode is: %s" % token_json['errcode']
                print "errmsg is: %s" % token_json['errmsg']
            else:
                print result

    def __get_token_from_persistence_storage(self):
        try:
            token_result_set = sqlite3_get_token()
        except:
            self.__get_token_from_weixin_qy_api()
        finally:
            if token_result_set is None or token_result_set.count() == 0:
                self.__get_token_from_weixin_qy_api()
                token_result_set = sqlite3_get_token()
                access_token = token_result_set[0][0]
                expire_time = token_result_set[0][1]
            else:
                access_token = token_result_set[0][0]
                expire_time = token_result_set[0][1]
        expire_time = datetime.datetime.strptime(expire_time, '%Y-%m-%d %H:%M:%S.%f')
        now_time = datetime.datetime.now()
        if now_time < expire_time:
            # print "The token is %s" % access_token
            # print "The token will expire on %s" % expire_time
            return access_token
        else:
            self.__get_token_from_weixin_qy_api()
            return self.__get_token_from_persistence_storage()

    @staticmethod
    def __is_token_expired():
        try:
            token_result_set = sqlite3_get_token()
        except:
            sys.exit(1)
        expire_time = token_result_set[0][1]
        expire_time = datetime.datetime.strptime(expire_time, '%Y-%m-%d %H:%M:%S.%f')
        now_time = datetime.datetime.now()
        if now_time < expire_time:
            return False
        else:
            return True

    def get(self):
        return self.__get_token_from_persistence_storage()