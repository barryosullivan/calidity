"""
***User Interface Views***
"""
from django.shortcuts import render, HttpResponse
from .models import *


#Index Page for the website
def index( request ):
    temperatures = Temperature.objects.all().order_by('-time')[:96]
    temperatures = reversed(temperatures)
    user_preferences = User_Setting.objects.get()
    context = {
        'temperatures' : temperatures,
        'user_preference' : user_preferences,
    }
    return render( request, 'interface/index.html', context )

def settings( request ):
   user_preferences = User_Setting.objects.get()
   context = {
      'user_preference': user_preferences,
   }
   return render( request, 'interface/settings.html', context )