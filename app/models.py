from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    def description(self):
        return "spilleren " + self.name

    def __unicode__(self):
        return self.name

class Set(models.Model):
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    setNumber = models.IntegerField()
    match = models.ForeignKey("SingleMatch", related_name="sets")

class Club(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    def description(self):
        return "klubben " + self.name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

class Tournament(models.Model):
    name = models.CharField(max_length=30)
    cupID = models.IntegerField(primary_key=True)
    cupASSistName = models.CharField(max_length=30)
    host = models.ForeignKey(Club, related_name="tournaments", null=True)
    #Null because some tournaments don't have a hosting club
    fromDate = models.DateField()
    toDate = models.DateField()

    def description(self):
        return "turneringen " + self.name + " som ble spillt " + str(self.fromDate) +  " og arrangert av " + self.host.name

    def save(self, force_insert=False, force_update=False, using=None):
        self.host.save()
        super(Tournament, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['fromDate']

    def detailed_string_representation(self):
        s = u"<p>name: " + self.name + u"\n</br>"
        s += u"id: " + str(self.cupID) + u"\n</br>"
        s += u"cupASSistName: " + self.cupASSistName + u"\n</br>"
        s += u"host: " + unicode(self.host) + u"\n</br>"
        s += u"from: " + str(self.fromDate) + u"\n</br>"
        s += u"to: " + str(self.toDate) + u"\n</br>"
        s += u"</p>"
        return s

class Participants(models.Model):
    tournament = models.ForeignKey(Tournament, related_name="participants")
    player = models.ForeignKey(Player, related_name="participated_Tournaments")

class SingleMatch(models.Model):
    matchNumber = models.IntegerField()
    tournament = models.ForeignKey(Tournament, related_name="matches")
    winner = models.ForeignKey(Player, related_name="victories")
    loser = models.ForeignKey(Player, related_name="losses")
    winnerClub = models.ForeignKey(Club, related_name="victories")
    loserClub = models.ForeignKey(Club, related_name="losses")
    score = models.CharField(max_length=12)
    type = models.CharField(max_length=30)


def get_or_create_model(model, **key):
    try:
        obj = model.objects.get(**key)
    except model.DoesNotExist:
        obj = model(**key)
    return obj