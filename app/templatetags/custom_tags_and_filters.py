# This Python file uses the following encoding: utf-8


import urllib
from django.template import Library

register = Library()

@register.filter(name="redirect")
def redirect(value, arg):
    string = '<a href="?'#warning
    string += urllib.urlencode({'q':arg}, doseq=1)# problemet ligger ikke i urlencode, den ligger i arg
    #doseq=1 for å få den nye versjonen som håndterer unicode
    string += '">' + value + '</a>'
    return string