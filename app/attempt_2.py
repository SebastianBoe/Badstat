# This Python file uses the following encoding: utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response
from app.models import Club, Tournament

#Coded in preorder with respect to function calls

def attempt_2_at_interpreter(query):
    return Interpreter(query.lower()).interpret_and_render()

class Interpreter:
    def __init__(self, query):
        self.query = query
        self.queryables = self.get_queryables()
        self.base_context = {'query': query}

    def get_queryables(self):
        queryables = []
        [queryables.extend(queryable_container.get_queryable_objects()) for queryable_container in self.get_containers()]
        return queryables

    def get_containers(self):#Her må det hardkodes inn alle containers, begynner med bare klubber
        containers = list()
        #Nye containers inn her
        containers.append(Club_container())
        containers.append(Tournament_container())
        containers.append(Misc_container())
        return containers

    def interpret_and_render(self):
        """
        Finds the most fitting queryable-query match.
        If several are of equal compatibility, then a disambiguity request will be returned.
        Else a rendered template will be returned.
        """
        unique_match = [queryable for queryable in self.queryables if queryable.uniquely_matches(self.query)]
        if unique_match:
            return unique_match[0].render(self.base_context)
        else:
            ambiguous_matches = [queryable for queryable in self.queryables if queryable.ambiguously_matches(self.query)]
            if len(ambiguous_matches) == 0:
                return render_to_response('search_form.html')
            elif len(ambiguous_matches) == 1:
                return ambiguous_matches[0].render(self.base_context)
            else:
                return self.disambiguation_request(ambiguous_matches)

    def disambiguation_request(self, ambiguous_matches):
        self.base_context.update({'queryables':ambiguous_matches})
        return render_to_response('disambiguation_request.html', self.base_context)

class Queryable():
    def __init__(self, id, ambiguous_id, context, template):
        self.id = id
        self.ambiguous_id = ambiguous_id
        self.context = context
        self.template = template

    def __unicode__(self):
        return unicode(self.ambiguous_id)

    def uniquely_matches(self, query):
        return self.id.lower() == query

    def ambiguously_matches(self, query):
        return self.ambiguous_id.lower() == query

    def render(self, base_context):
        self.context.update(base_context)
        return render_to_response(self.template, self.context)

class Club_container():
    def get_queryable_objects(self):
       return [self.create_queryable_club(club) for club in Club.objects.all()]

    def create_queryable_club(self, club):
        return Queryable(id=club.description(), ambiguous_id=club.name, context={'club':club}, template='club.html')

class Tournament_container():
    def get_queryable_objects(self):
       return [self.create_queryable_tournament(tournament) for tournament in Tournament.objects.all()]

    def create_queryable_tournament(self, tournament):
        return Queryable(id=tournament.description(), ambiguous_id=tournament.name, context={'tournament' : tournament}, template='tournament.html')

class Misc_container():
    def get_queryable_objects(self):
        return \
        [
            Queryable(id="klubber", ambiguous_id="klubber", context={'clubs':Club.objects.all()}, template='clubs.html'),
            Queryable(id="turneringer", ambiguous_id="turneringer", context={'tournaments':Tournament.objects.all()}, template='tournaments.html')
        ]