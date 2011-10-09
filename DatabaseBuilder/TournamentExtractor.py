# This Python file uses the following encoding: utf-8

# Set the DJANGO_SETTINGS_MODULE environment variable.
import os
os.environ['DJANGO_SETTINGS_MODULE'] = "Badminton.settings"

import string
import re
from datetime import date
from Badminton.app.models import Tournament
from Badminton.settings import tournamentUrl, uselessTournamentIDs, badminton_invitation_identifier
from Badminton.util import getFile

class TournamentExtractor():
    def __init__(self, cupID):
        self.cupID = str(cupID)
        self.html = getFile(tournamentUrl + self.cupID).decode("latin1")
        self.__tournament = Tournament()

    def initialize_tournament(self):
        if not self.is_badminton_invitation():
            raise Exception("Not a badminton invitation")

        self.__extractFields()
        return self.__tournament

    def is_badminton_invitation(self):
        return badminton_invitation_identifier in self.html and int(self.cupID) not in uselessTournamentIDs

    def __extractFields(self):
        t = self.__tournament
        self.__extractDates()
        t.cupASSistName = self.extract_CupASSist_name()
        t.host = self.extract_host()
        t.name = self.extract_name()
        t.cupID = self.cupID

    def __extractDates(self):
        t = self.__tournament
        t.toDate = self.__extractDate(pattern = '(?<=Til:</td><td>)[^<]*(?=<)')
        t.fromDate = self.__extractDate(pattern = '(?<=Fra: </td><td>)[^<]+(?=<)')
        self.__fixNoneDate()

    def __extractDate(self, pattern):
        try:
            string = re.search(pattern, self.html).group(0)
            tupleDate = self.__cut0Prefix(string[0:2]), self.__cut0Prefix(string[3:5]), self.__cut0Prefix(string[6:])
            return date(day = int(tupleDate[0]) , month = int(tupleDate[1]) , year = int(tupleDate[2]) )
        except Exception:
            pass

    def __cut0Prefix(self, param):
        if param[0] == '0':
            return param[1:]
        return param

    def __fixNoneDate(self):
        self.__tournament.fromDate = self.__tournament.fromDate or self.__tournament.toDate
        self.__tournament.toDate = self.__tournament.toDate or self.__tournament.fromDate

    def extract_host(self):
        pattern = '(?<=Arrangør</td><td>)[^<]*(?=<)'
        name = re.search(pattern, self.html).group(0)
        from Badminton.app.models import get_or_create_model, Club

        if name != "":
            return get_or_create_model(Club, name = name)
        else:
            #Ble problemer med id 686
            #Nei dette var en for stygg hack, må få en penere løsning
            return get_or_create_model(Club, name = u"Ukjent arrangør")

    def extract_name(self):
        pattern = '(?<=Arrangement</td><td>)[^<]+(?=<)'
        name = re.search(pattern, self.html).group(0)
        if self.cupID == "767":
            name = u"Nye Fjær 2011."
        return name


    def extract_CupASSist_name(self):
        from Badminton.settings import corruptedCupASSistnames
        pattern = '(?<=turn=)[^"]+(?=")'

        if int(self.cupID) in corruptedCupASSistnames:
            return corruptedCupASSistnames[int(self.cupID)]

        cupASSistName =  re.search(pattern, self.html).group(0)
        return self.__fix_odd_CupASSist_name_prefixes(cupASSistName)

    def __fix_odd_CupASSist_name_prefixes(self, cupASSistName):
        prefixes = [".com/", "tknavn="]
        for prefix in prefixes:
            if prefix in cupASSistName:
                nameStartIndex = string.index(cupASSistName, prefix) + len(prefix)
                cupASSistName = cupASSistName[nameStartIndex:]

        return cupASSistName