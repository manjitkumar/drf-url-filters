from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=254)
    rating = models.FloatField(null=True)
    teams = models.ManyToManyField(
        'Team',
        through='Membership',
        through_fields=('team', 'player')
    )
    install_ts = models.DateTimeField(auto_now_add=True, blank=True)
    update_ts = models.DateTimeField(auto_now_add=True, blank=True)


class Team(models.Model):
    name = models.CharField(max_length=254)
    rating = models.FloatField(null=True)
    players = models.ManyToManyField(
        'Player',
        through='Membership',
        through_fields=('team', 'player')
    )
    install_ts = models.DateTimeField(auto_now_add=True, blank=True)
    update_ts = models.DateTimeField(auto_now_add=True, blank=True)


class Membership(models.Model):
    team = models.ForeignKey('Team')
    player = models.ForeignKey('Player')
    is_active = models.BooleanField(default=True)
    date_of_joining = models.DateTimeField()
    install_ts = models.DateTimeField(auto_now_add=True, blank=True)
    update_ts = models.DateTimeField(auto_now_add=True, blank=True)
