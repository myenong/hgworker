# -*- coding: utf8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class weixin_token(models.Model):
    # 如果没有models.AutoField，默认会创建一个id的自增列
    access_token = models.TextField()
    expires_in = models.TextField()
    expires_on = models.TextField()
    is_expired = models.IntegerField(default=0)

    class Meta:
        db_table = 'weixin_token'


class weixin_account(models.Model):
    # 如果没有models.AutoField，默认会创建一个id的自增列
    name = models.TextField()
    corpid = models.TextField()
    secret = models.TextField()
    current = models.IntegerField(default=0)

    class Meta:
        db_table = 'weixin_account'