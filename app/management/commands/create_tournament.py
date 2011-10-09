from django.core.management.base import BaseCommand
from Badminton.DatabaseBuilder.TournamentExtractor import TournamentExtractor
import sys

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if len(sys.argv) == 3:
            TournamentExtractor(sys.argv[2]).initialize_tournament().save()
        else:
            print "You must enter a cupID"