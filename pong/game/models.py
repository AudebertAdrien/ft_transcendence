# /pong/game/models.py

from django.db import models
from django.contrib.auth.models import User

User.add_to_class('auth_token', models.CharField(max_length=100, null=True, blank=True, unique=True))

class Player(models.Model):
    name = models.CharField(max_length=100)
    total_match = models.PositiveSmallIntegerField(default=0)
    total_win = models.PositiveSmallIntegerField(default=0)
    p_win = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    num_participated_tournaments = models.PositiveSmallIntegerField(default=0)
    num_won_tournaments = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name 

class Tournoi(models.Model):
    name = models.CharField(max_length=200)
    nbr_player = models.PositiveSmallIntegerField()
    date = models.DateField(auto_now_add=True)
    winner = models.ForeignKey('Player', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Match(models.Model):
    player1 = models.CharField(max_length=100)
    player2 = models.CharField(max_length=100)
    score_player1 = models.PositiveSmallIntegerField()
    score_player2 = models.PositiveSmallIntegerField()
    winner = models.CharField(max_length=100)
    nbr_ball_touch_p1 = models.PositiveIntegerField()
    nbr_ball_touch_p2 = models.PositiveIntegerField()
    duration = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    is_tournoi = models.BooleanField()
    tournoi = models.ForeignKey('Tournoi', related_name='matches', on_delete=models.SET_NULL, null=True)

    def clean(self):
        if self.score_player1 < 0 or self.score_player2 < 0:
            raise ValidationError('Les scores doivent être positifs.')
        if self.score_player1 > self.score_player2 and self.winner != self.player1:
            raise ValidationError('Le gagnant ne correspond pas aux scores.')
        if self.score_player2 > self.score_player1 and self.winner != self.player2:
            raise ValidationError('Le gagnant ne correspond pas aux scores.')
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.player1.name} vs {self.player2.name}"