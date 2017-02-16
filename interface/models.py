"""
***User Interface models***
"""
from django.db import models

#Stores All the weather data
class Temperature(models.Model):
    time = models.DateTimeField(auto_now_add=True, primary_key=True)
    external_c = models.IntegerField()
    internal_c = models.IntegerField()
    wind_kph = models.IntegerField()
    humidity = models.IntegerField()
    chance_of_precipitation = models.IntegerField()
    expected_high = models.IntegerField()
    expected_low = models.IntegerField()

#Store Global comfort settings
class User_Setting(models.Model):
	boiler_high = models.IntegerField()
	boiler_low = models.IntegerField()
	margin_of_error = models.IntegerField()
	ideal_temp = models.IntegerField()
	updated = models.DateTimeField(auto_now=True)