"""
***User Interface models***
"""
from django.db import models

#stores all the recorded temps
class Temperature(models.Model):
    time = models.DateTimeField(auto_now_add=True, primary_key=True)
    external_c = models.FloatField()
    internal_c = models.FloatField()

#stores all the weather data
class Weather(models.Model):
    time = models.DateTimeField(auto_now_add=True, primary_key=True)
    conditions = models.CharField(max_length = 20)
    humidity = models.FloatField()
    wind_kph = models.IntegerField()
    chance_rain = models.IntegerField()
    high = models.FloatField()
    low = models.FloatField()
    snow = models.FloatField()

#Stores user settings
class User_Setting(models.Model):
	margin_of_error = models.IntegerField()
	ideal_temp = models.IntegerField()
#Override option

#Stores data about the heating system
#In this instance - a boiler
class Heating_System(models.Model):
    status = models.BooleanField(default=False)
    fuel_remaining = models.FloatField()
    burn_rate = models.FloatField()

class Building(models.Model):
    windows = models.BooleanField(default=False)