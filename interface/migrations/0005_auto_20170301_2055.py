# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0004_auto_20170301_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperature',
            name='humidity',
            field=models.FloatField(),
        ),
    ]