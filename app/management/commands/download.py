# This Python file uses the following encoding: utf-8

from django.core.management.base import BaseCommand
from Badminton.DatabaseBuilder.TournamentExtractor import TournamentExtractor
import sys

class Command(BaseCommand):
    def repeating_tournament_extraction(self):
        if len(sys.argv) == 3:
            id = sys.argv[2]
        else:
            id = int(raw_input("cupID="))

        while id != -1:
            te = TournamentExtractor(id)
            if te.is_badminton_invitation():
                print unicode(te.initialize_tournament())
            else:
                print "That's not a badminton tournament!"
            id = int(raw_input("cupID="))

    def handle(self, *args, **kwargs):
        self.repeating_tournament_extraction()
        #self.save_a_tournament()