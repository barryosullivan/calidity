"""
***User Interface models***
"""
from django.db import models

ECONOMICAL = "ECONOMICAL"
COMFORT = "COMFORT"

heating_choices = (
    (ECONOMICAL, "Economical"),
    (COMFORT, "Comfort"),
)
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
    setting = models.CharField(max_length = 10, choices = heating_choices, default="COMFORT")
    ideal_temp = models.IntegerField(default=19)
    system_override = models.BooleanField(default=False)

#Stores data about the heating system
#In this instance - a boiler
class Heating_System(models.Model):
    status = models.BooleanField(default=False)
    fuel_remaining = models.FloatField()
    burn_rate = models.FloatField()

#data model for the building 
class Building(models.Model):
    windows = models.BooleanField(default=False)
	
#data model storing system alerts
class Alert(models.Model):
    snow_expected = models.BooleanField(default=False)
    ice_expected = models.BooleanField(default=False)
    heatwave_expected = models.BooleanField(default=False)
    open_windows = models.BooleanField(default=False)