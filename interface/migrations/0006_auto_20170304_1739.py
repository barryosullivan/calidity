# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-04 17:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0005_auto_20170301_2055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_setting',
            name='boiler_high',
        ),
        migrations.RemoveField(
            model_name='user_setting',
            name='boiler_low',
        ),
        migrations.RemoveField(
            model_name='user_setting',
            name='updated',
        ),
    ]