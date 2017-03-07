"""
***User Interface Views***
"""
from django.shortcuts import render, HttpResponse
from .models import *


#Index Page for the website
def index( request ):
    temperatures = Temperature.objects.all().order_by('-time')[:96]
    temperatures = reversed(temperatures)
    current_temp = Temperature.objects.order_by('-time').first()
    user_preferences = User_Setting.objects.get()
    heating_system = Heating_System.objects.get()
    weather = Weather.objects.order_by('-time').first()

    hours_remaining = heating_system.fuel_remaining / heating_system.burn_rate
    open_windows = 'Yes' if current_temp.internal_c > 25 else 'No'
    snow_expected = 'Yes' if weather.snow > 0 else 'No'
    ice_expected = 'Yes' if weather.low < 0 else 'No'
    heatwave_expected = 'Yes' if weather.high > 30 else 'No'

    context = {
        'temperatures' : temperatures,
        'current_temp' : current_temp,
        'user_preference' : user_preferences,
        'heating_system' : heating_system,
        'weather' : weather,
        'hours_remaining' : hours_remaining,
        'open_windows' : open_windows,
        'snow_expected' : snow_expected,
        'ice_expected' : ice_expected,
        'heatwave_expected' : heatwave_expected,
    }
    return render( request, 'interface/index.html', context )

def settings( request ):
    user_preferences = User_Setting.objects.get()
    heating_system = Heating_System.objects.get()
    building = Building.objects.get()
    context = {
        'user_preference': user_preferences,
        'heating_system' : heating_system,
        'building' : building,
    }
    if request.method == 'POST':
        return render( request, 'interface/settings.html', context )
    else: 
        return render( request, 'interface/settings.html', context )