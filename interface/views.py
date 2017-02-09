"""
***User Interface Views***
"""
from django.shortcuts import render, HttpResponse



#Index Page for the website
def index( request ):
    context = {
    }
    return render( request, 'interface/index.html', context )