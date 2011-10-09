# This Python file uses the following encoding: utf-8

from urllib import urlopen

def getFile(url):
    f = urlopen(url)
    file = f.read()
    f.close()
    return file

def string_distance(a, b):
    pass