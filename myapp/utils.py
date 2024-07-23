from myapp.models import Player, Tournoi, Match
from django.core.exceptions import ValidationError

def create_player(name):
    player = Player(name=name)
    player.save()
    return player

def create_tournoi(name, nbr_player, date, winner=None):
    tournoi = Tournoi(name=name, nbr_player=nbr_player, date=date, winner=winner)
    tournoi.save()
    return tournoi

def create_match(player1, player2, score_player1=0, score_player2=0, winner=None, nbr_ball_touch_p1=0, nbr_ball_touch_p2=0, duration=None, is_tournoi=False, tournoi=None):
    match = Match(
        player1=player1,
        player2=player2,
        score_player1=score_player1,
        score_player2=score_player2,
        winner=winner,
        nbr_ball_touch_p1=nbr_ball_touch_p1,
        nbr_ball_touch_p2=nbr_ball_touch_p2,
        duration=duration,
        is_tournoi=is_tournoi,
        tournoi=tournoi
    )
    match.save()
    return match

def complete_match(match_id, score_player1, score_player2, nbr_ball_touch_p1, nbr_ball_touch_p2, duration):
    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        raise ValidationError(f"Match with id {match_id} does not exist")

    match.score_player1 = score_player1
    match.score_player2 = score_player2
    match.nbr_ball_touch_p1 = nbr_ball_touch_p1
    match.nbr_ball_touch_p2 = nbr_ball_touch_p2
    match.duration = duration

    if score_player1 > score_player2:
        match.winner = match.player1
    elif score_player2 > score_player1:
        match.winner = match.player2
    else:
        match.winner = None

    match.save()
    return match

def complete_tournoi(tournoi_id, player):
    try:
        tournoi = Tournoi.objects.get(id = tournoi_id)
    except Tournoi.DoesNotExist:
        raise ValidationError(f"Tournoi with id {tournoi_id} does not exist")
    
    tournoi.winner = player
    tournoi.save()
    return tournoi