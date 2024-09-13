from .models import Player, Tournoi, Match
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Max, Sum, F
from datetime import timedelta
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.db.models import Q

def handle_game_data(p1, p2, s_p1, s_p2, bt_p1, bt_2, dur, is_tournoi, name_tournament):
    try:
        print("Here !!!!!!!!")
        player_1 = get_or_create_player(p1)
        print("FIRST PLAYER REGISTERD")
        player_2 = get_or_create_player(p2)
        print("SECOND PLAYER REGISTERD")


        if (not player_1 or not player_2) :
            print("AIIEJJDFKJBDBKJJKB PROBLEME ORIOL ")
        print("CHAKU & THEOUCHE are the BEST")
        create_match(player_1, player_2, s_p1, s_p2, bt_p1, bt_2, dur, is_tournoi, name_tournament)
        print("and ADRIANO is the PEST")

        update_player_statistics(p1)
        print("END UPDATE FISRT PLAYER")
        update_player_statistics(p2)
        print("END UPDATE SECOND PLAYER")
        
    except Exception as e:
        print(f"Error in endfortheouche: {e}")


def get_or_create_player(name):
    print("Get or create player")
    # Utilise get_or_create pour chercher un joueur existant ou en créer un nouveau avec les valeurs par défaut
    player, created = Player.objects.get_or_create(
        name=name,
        defaults={
            'total_match': 0,
            'total_win': 0,
            'p_win': None,
            'num_participated_tournaments': 0,
            'num_won_tournaments': 0
        }
    )
    if created:
        print("Player created")
    else:
        print("Player exists")
    return player



def create_tournoi(name, nbr_player, date, winner):
    tournoi = Tournoi(name=name, nbr_player=nbr_player, date=date, winner=winner)
    tournoi.save()
    return tournoi

def create_match(player1, player2, score_player1, score_player2, nbr_ball_touch_p1, nbr_ball_touch_p2, duration, is_tournoi, tournoi):
    match = Match(
        player1=player1,
        player2=player2,
        score_player1=score_player1,
        score_player2=score_player2,
        nbr_ball_touch_p1=nbr_ball_touch_p1,
        nbr_ball_touch_p2=nbr_ball_touch_p2,
        duration=duration,
        is_tournoi=is_tournoi,
        tournoi=tournoi
    )

    if score_player1 > score_player2:
        match.winner = match.player1
    elif score_player2 > score_player1:
        match.winner = match.player2
    else:
        match.winner = None
    
    match.save()
    return match

def update_player_statistics(player_name):
    print("UPDATED DATA")
    player = get_object_or_404(Player, name=player_name)


    matches = Match.objects.filter(Q(player1=player) | Q(player2=player))

    total_match = matches.count()

    
    # avoid dividing by 0
    if total_match == 0:
        player.total_match = total_match
        player.total_win = 0
        player.p_win = 0
        player.num_participated_tournaments = 0
        player.num_won_tournaments = 0
        player.save()
        return

    nb_win =0
    
    for match in matches :
        if match.winner == player:
            nb_win = nb_win + 1


    #won_matches = Match.objects.filter(winner=player)
    #part_tourn_as_p1 = Tournoi.objects.filter(matches__is_tournoi=True, matches__matches_as_player1=player)
    #part_tourn_as_p2 = Tournoi.objects.filter(matches__is_tournoi=True, matches__matches_as_player2=player)
    #won_tourn = Tournoi.objects.filter(winner=player) 


    #total_win = won_matches.count()


    p_win = (nb_win/ total_match) * 100
    
    #total_tourn_p = part_tourn_as_p1.count() + part_tourn_as_p2.count()
    #total_win_tourn = won_tourn.count()
    #p_win_tourn = (total_win_tourn / total_tourn_p) * 100 if total_tourn_p else 0
 
    player.total_match = total_match
    player.total_win = total_win
    player.p_win = p_win
    # player.num_participated_tournaments = total_tourn_p
    #player.num_won_tournaments = total_win_tourn 

    player.save()

def get_player_p_win(player_name):
    player = get_object_or_404(Player, name=player_name)
    return player.p_win

def create_tournament(name, nbr_player):
    print("tournoi created!!!")
    tournoi=Tournoi(name=name, nbr_player=nbr_player, winner=None)
    tournoi.save()
    print(f"tournoi name : {tournoi.name}  *******!*!*!*!**!*!**!*!*!*!*!*!*!*!*!*")
    return tournoi

def update_tournament(name_tournoi, winner_name):
    tournoi = get_object_or_404(Tournoi, name=name_tournoi)
    winner_p = get_object_or_404(Player, name=winner_name)
    print(f"in update tourna - tournoi name : {tournoi.name}  *******!*!*!*!**!*!**!*!*!*!*!*!*!*!*!*")
    print(f"in update tourna - winner is : {winner_p.name}  *******!*!*!*!**!*!**!*!*!*!*!*!*!*!*!*")

    tournoi.winner = winner_p
    print(f"in update tourna - TOURNOI winner is : {tournoi.winner.name}  *******!*!*!*!**!*!**!*!*!*!*!*!*!*!*!*")
    tournoi.save()


def getlen():
    return Tournoi.objects.count()
