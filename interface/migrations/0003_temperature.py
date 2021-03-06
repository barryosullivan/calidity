# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0002_delete_temperature'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('time', models.DateTimeField(auto_now_add=True, primary_key=True, serialize=False)),
                ('external_c', models.IntegerField()),
                ('internal_c', models.IntegerField()),
                ('wind_kph', models.IntegerField()),
                ('humidity', models.IntegerField()),
                ('chance_of_precipitation', models.IntegerField()),
                ('expected_high', models.IntegerField()),
                ('expected_low', models.IntegerField()),
            ],
        ),
    ]
