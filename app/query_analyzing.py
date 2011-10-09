from django.http import HttpResponse
from django.shortcuts import render_to_response
from util import query_distance
from Badminton.app.models import *

def listener_register(query):
    """
    All listeners must be added to this list.
    """
    return  [club_overview_listener(query)]

class controller():
    """
    Tries to guess as best as possible what the query was for.
    If neccessary it will ask the user to clarify.
    """
    def __init__(self, query):
        self.query = query
        self.vagueness_level = 0
        self.listeners = listener_register(query)
        self.matches = []
        for listener in self.listeners:
            self.matches.extend(listener.exact_matches())

    def response(self):
        if len(self.matches) == 0:
            self.vagueness_level += 1
            self.__find_partial_matches()
            return self.response()
        elif len(self.matches) == 1:
            return self.matches[0].render()
        elif len(self.matches) > 1:
            return self.__user_excplicitation_request()

    def __find_partial_matches(self):
        self.matches = []
        for listener in self.listeners:
            self.matches.append(listener.partial_matches(self.vagueness_level))

    def __user_excplicitation_request(self):
        context = {"match_objects":self.matches, "query": self.query}
        return render_to_response('search_clarification_request.html', context)

class listener_interface():
    """
    A listener is something that has a set of objects, and listens to queries.
    If it deems that the query matches one of its objects it will return return the object encapsulated in a
    match object.
    """
    def __init__(self, query):
        self.query = query

    def exact_matches(self):
        """
        Returns a list of matching objects or an empty list if there were none.
        """
        pass

    def partial_matches(self, matching_algorithm, vagueness_level):
        """
        Returns a list of partially matching match_objects.
        """
        pass

class match_object():
    """
    An object containing a human readable description
     and an identifier that will uniquely identify it if queried for.
    """
    def __init__(self, description, id, listener, object=None):
        self.description = description
        self.id = id
        self.listener = listener
        self.object = object

    def render(self):
        return self.listener.render()

class club_overview_listener():
    def __init__(self, query):
        self.query = query

    def exact_matches(self):
        if "klubber" == self.query.lower():
            return [self.__club_match_object()]
        return []

    def __club_match_object(self):
        return match_object("oversikt over alle klubbene", "klubber", self)

    def render(self):
        return render_to_response('clubs.html', {'clubs': Club.objects.all(), 'query':'klubber'})

    def partial_matches(self, vagueness_level):
        if query_distance(self.query, "klubber") <= vagueness_level:
            return [self.__club_match_object()]
        return []

class club_listener():
    def __init__(self, query):
        self.query = query

    def exact_matches(self):
        if Club.objects.filter(name__iexact=self.query).exists():
            self.potential_hit = Club.objects.get(name_iexact=self.query)
            return [self.potential_hit]
        return []

    def render(self):
        return render_to_response('club.html', {'club': self.potential_hit, 'query' : self.query})

    def partial_matches(self, vagueness_level):
        matches = [match_object(club.description(), club.name, self, club) for club in Club.objects.all() if query_distance(self.query, club.name) <= vagueness_level]
        if matches:
            self.potential_hit = matches[0]
        return matches













