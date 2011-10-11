# This Python file uses the following encoding: utf-8
import string
import urllib2, cookielib, re
from Badminton.app.models import *

def download_participants_document(cupASSistName):
   """
   This method returns an html document containing
   the registered players for the tournament with the given cupASSistName.
   First it visits cupassist.com/pamelding/redirect.php, to recieve a cookie used for navigation.
   Lastly it visits /pamelding/vis_pamelding.php for the desired document.
   """
   opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()), urllib2.HTTPRedirectHandler())
   opener.open("http://www.cupassist.com/pamelding/redirect.php?tknavn=" + cupASSistName)
   return opener.open("http://www.cupassist.com/pamelding/vis_paamelding.php").read()

def extract_single_players_name(html):
    start = '<tr><td>\s'
    middle = '[^</]+?'
    end = '\s</td><td>'
    pattern = '(?<=%s)%s(?=%s)' % (start, middle, end)
    return map(format_name, re.findall(pattern, html))

def format_name(name):
    """
    Takes a name of the form "<Last Name>, <Rest of name>" and retuns a name of the form:
    "<First name> <name 2> <name 3> ... <last name>".

    >>> format_name("Bøe, Sebastian Awesome") == "Sebastian Awesome Bøe"
    True
    """
    comma_index = string.find(name, ",")
    return name[comma_index + 2:] + " " + name[:comma_index]

def update_database(tournament, player_names):
    for name in player_names:
        if not player_in_database(name):
            register_player(name)

        p = Participants()
        p.player = find_player(name)
        p.tournament = tournament
        p.save()