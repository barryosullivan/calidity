# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 17:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0008_auto_20170304_2216'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('windows', models.BooleanField(default=False)),
            ],
        ),
    ]