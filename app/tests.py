# This Python file uses the following encoding: utf-8

from django.test import TestCase
from datetime import date
from Badminton.DatabaseBuilder.TournamentExtractor import TournamentExtractor
from Badminton.DatabaseBuilder.ParticipantsExtractor import *

class SimpleTest(TestCase):
    def general_tournament_test(self, name, cupID, cupASSistName, host_name, fromDate, toDate, is_badminton_invitation=True):
        tournament_extractor = TournamentExtractor(cupID)
        self.failUnlessEqual(tournament_extractor.is_badminton_invitation(), is_badminton_invitation)
        if tournament_extractor.is_badminton_invitation():
            tournament = tournament_extractor.initialize_tournament()
            self.failUnlessEqual(tournament.name, name)
            self.failUnlessEqual(tournament.cupID, cupID)
            self.failUnlessEqual(tournament.cupASSistName, cupASSistName)
            self.failUnlessEqual(tournament.host.name, host_name)
            if fromDate is None:
                self.failUnlessEqual(tournament.fromDate, toDate)
            if toDate is None:
                self.failUnlessEqual(tournament.toDate, fromDate)


    def test_tournament_extractor_ungdomsspretten(self):
        self.general_tournament_test("Ungdomsspretten 2010", "454", "ungdomsspretten2010", "Stavanger Badmintonklubb",
                                     date(2010, 9, 18), date(2010, 9, 18))

    def test_foreign_characters(self):
        self.general_tournament_test(u"Askøy senior 2010", "547", "askoysenior2010", u"Askøy Badmintonklubb",
                                     date(2010, 10, 10), date(2010, 10, 10))

    def test_fix_None_Date(self):
        t = TournamentExtractor(200).initialize_tournament()
        self.failUnlessEqual(t.toDate, t.fromDate)
        self.failUnlessEqual(t.toDate, date(2009,12,28))

    def test_tournament_extractor_kbkranking(self):
        self.general_tournament_test(
            name = "September ranking U13, U17 og NR",
            cupID= "446",
            cupASSistName= "kbkranking10",
            host_name="Kristiansand Badmintonklubb",
            fromDate=date(2010,9,17),
            toDate=date(2010,9,19))

    def test_participants_extractor(self):
        players = extract_single_players_name(download_participants_document('ungdomsspretten2010'))
        self.failUnlessEqual(len(players), 29)
        self.failUnlessEqual("Sebastian Awesome Boe", format_name("Boe, Sebastian Awesome"))