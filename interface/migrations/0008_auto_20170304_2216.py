# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-04 22:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0007_boiler'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('time', models.DateTimeField(auto_now_add=True, primary_key=True, serialize=False)),
                ('conditions', models.CharField(max_length=20)),
                ('humidity', models.FloatField()),
                ('wind_kph', models.IntegerField()),
                ('chance_rain', models.IntegerField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('snow', models.FloatField()),
            ],
        ),
        migrations.RenameModel(
            old_name='Boiler',
            new_name='Heating_System',
        ),
        migrations.RemoveField(
            model_name='temperature',
            name='chance_of_precipitation',
        ),
        migrations.RemoveField(
            model_name='temperature',
            name='expected_high',
        ),
        migrations.RemoveField(
            model_name='temperature',
            name='expected_low',
        ),
        migrations.RemoveField(
            model_name='temperature',
            name='humidity',
        ),
        migrations.RemoveField(
            model_name='temperature',
            name='wind_kph',
        ),
    ]
