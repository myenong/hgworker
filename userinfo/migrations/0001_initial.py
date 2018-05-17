# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='weixin_account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('corpid', models.TextField()),
                ('secret', models.TextField()),
                ('current', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'weixin_account',
            },
        ),
        migrations.CreateModel(
            name='weixin_token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('access_token', models.TextField()),
                ('expires_in', models.TextField()),
                ('expires_on', models.TextField()),
                ('is_expired', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'weixin_token',
            },
        ),
    ]
