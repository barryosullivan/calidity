from django.contrib import admin
from interface.models import Temperature, User_Setting, Weather, Heating_System

# Register your models here.
admin.site.register(Temperature)

admin.site.register(User_Setting)

admin.site.register(Weather)

admin.site.register(Heating_System)