"""
***User Interface url's***
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    #localhost:8000/Calidity
    url( r'^$', views.index, name='index' ),
]