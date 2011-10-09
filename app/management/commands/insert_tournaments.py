from django.core.management.base import BaseCommand
from Badminton.DatabaseBuilder.TournamentExtractor import TournamentExtractor
import sys

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if len(sys.argv) == 3:
            TournamentExtractor(sys.argv[2]).initialize_tournament().save()

        elif len(sys.argv) == 4:
            for id in range(int(sys.argv[2]), int(sys.argv[3])):
                extractor = TournamentExtractor(id)
                if extractor.is_badminton_invitation():
                    extractor.initialize_tournament().save()

        else:
            print "you must enter either a tournament id to download, or a range of ids"