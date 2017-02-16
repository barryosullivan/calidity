"""
* Calidity URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    #localhost:8000
    url(r'^', include('interface.urls')),
    
	#localhost:8000/Calidity 
    url(r'^Calidity/', include('interface.urls')),

    #localhost:8000/admin
    url(r'^admin/', include(admin.site.urls)),
]