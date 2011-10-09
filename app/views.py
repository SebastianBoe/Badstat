# This Python file uses the following encoding: utf-8
from django.shortcuts import render_to_response
from Badminton.app.models import *

def create_list_of_lists(tournament_hits):
    container_list = []
    for tournament in tournament_hits:
        tournament_has_been_appended = False
        for sub_list in container_list:
            if sub_list[0].host == tournament.host:
                sub_list.append(tournament)
                tournament_has_been_appended = True
                break
        if not tournament_has_been_appended:
            container_list.append([tournament])
    return container_list

def request_more_information_about_tournament(request, tournament_hits, query):
    #Har lyst på språklig error feedback som et prinsipp. For å få et "komplisert" error tilbake melding må jeg mate
    #templaten en liste med lister av turneringer. Der hver liste med turneringer representerer en klubb sine turneringer
    #listen med turneringer bør være sortert chronologisk
    list_of_lists_of_tournaments = create_list_of_lists(tournament_hits)
    context_dict = {'list_of_lists_of_tournaments': list_of_lists_of_tournaments, 'query': query}
    return render_to_response('../templates/tournament_search_clarification_request.html', context_dict)

def is_clubs(query):
    return query == "klubber"

def new_handler(request):
    query = request.GET['q']
    d = dict()
    d.update({is_clubs : clubs})

    for key, value in d:
        if key(query):
            return value(query)

def desired_search_handler(request):
    query = request.GET['q'].lower()
    from query_analyzing import controller
    return controller(query).response()

def handle_search_request(request):
    #Kjente potensielle feil:
    #Potensiell ambiguity error om et turneringsnavn består kun av et tall, på mark 1
    # Hadde vært kult med en dict, der key var en funksjon som avgjorde basert på query
    # om det oppfyllte kravet til å bli vurdert og output var boolean
    # handle search returnerer da hva value funksjonen i dictet returnerer på queryet
    query = request.GET['q']
    d = dict()
    d.update({is_clubs : clubs})

    if is_clubs(query):
        return clubs(request)

    elif query == "turneringer":
        return tournaments(query)

    elif is_integer(query) and cupID_exists(int(query)):#1
        tournament = Tournament.objects.get(cupID=int(query))
        return render_to_response('tournament.html', {'tournament':tournament,'query':query})

    elif Tournament.objects.filter(name__iexact=query).exists():
        tournament_hits = Tournament.objects.filter(name__iexact=query)
        if tournament_hits.count() == 1:
            return render_to_response('tournament.html', {'tournament':tournament_hits[0], 'query':query})
        else:
            return request_more_information_about_tournament(request, tournament_hits, query)

    elif Club.objects.filter(name__iexact=query).exists():
        club = Club.objects.get(name__iexact=query)
        return render_to_response('club.html', {'club': club, 'query':query})

    else: return render_to_response('search_form.html')

def clubs(request):
    return render_to_response('clubs.html', {'clubs': Club.objects.all(), 'query':'klubber'})

def tournaments(request):
    return render_to_response('tournaments.html', {'tournaments' : Tournament.objects.all(), 'query':'tournaments'})

def search(request):
    if 'q' in request.GET:
        #return desired_search_handler(request)#YEah, her må vi endre for å få gammel kode
        from attempt_2 import attempt_2_at_interpreter
        return attempt_2_at_interpreter(request.GET['q'])
        return handle_search_request(request)
    return render_to_response('search_form.html')

def cupID_exists(query):
    return Tournament.objects.filter(cupID=int(query)).exists()

def is_integer(object):
    try:
        a = int(object)
        return True
    except:
        return False