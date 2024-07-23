from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 

class Tournoi(models.model):
    name = models.CharField(max_length=200)
    nbr_player = models.PositiveSmallIntegerField()
    date = models.DateField()
    winner = models.ForeignKey('Player', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Match(models.Model):
    player1 = models.ForeignKey('Player', related_query_name='match_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey('Player', related_query_name='match_as_player2', on_delete=models.CASCADE)
    score_player1 = models.PositiveSmallIntegerField()
    score_player2 = models.PositiveSmallIntegerField()
    winner = models.ForeignKey('Player', related_query_name='won_matches',on_delete=models.CASCADE)
    nbr_ball_touch_p1 = models.PositiveIntegerField()
    nbr_ball_touch_p2 = models.PositiveIntegerField()
    duration = models.DurationField()
    date = models.DateField(auto_now_add=True)
    is_tournoi = models.BooleanField()
    tournoi = models.ForeignKey('Tournoi', related_query_name='matches', on_delete=models.SET_NULL, null=True)

    def clean(self):
        if self.score_player1 < 0 or self.score_player2 < 0:
            raise ValidationError('Les scores doivent être positifs.')
        if self.score_player1 > self.score_player2 and self.winner != self.player1:
            raise ValidationError('Le gagnant ne correspond pas aux scores.')
        if self.score_player2 > self.score_player1 and self.winner != self.player2:
            raise ValidationError('Le gagnant ne correspond pas aux scores.')
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()  # Appel de la méthode clean() avant d'enregistrer
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.player1.name} vs {self.player2.name}"
