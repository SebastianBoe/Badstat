from urllib import urlopen

def query_distance(query, string):
    pass

def unique(list):
    set = {}
    map(set.__setitem__, list, [])
    return set.keys()

def getFile(url):
    f = urlopen(url)
    file = f.read()
    f.close()
    return file
