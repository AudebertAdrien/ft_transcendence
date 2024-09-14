from .models import Player, Tournoi, Match
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Max, Sum, F

from asgiref.sync import sync_to_async
from django.db.models import Q
import asyncio

players_name_list = []
tournament_participations = {}

def handle_game_data(p1, p2, s_p1, s_p2, bt_p1, bt_2, dur, is_tournoi, name_tournament):
    try:
        print("Here !!!!!!!!")
        #get_or_create_player(p1, p2)
        #print("FIRST PLAYER REGISTERD")
        #await sync_to_async(get_or_create_player)(p2)
        #print("SECOND PLAYER REGISTERD")

        print("CHAKU & THEOUCHE are the BEST")
        create_match(p1, p2, s_p1, s_p2, bt_p1, bt_2, dur, is_tournoi, name_tournament)
        print("and ADRIANO is the PEST")

        #update_player_statistics(p1)
        print("END UPDATE FISRT PLAYER")
        #update_player_statistics(p2)
        print("END UPDATE SECOND PLAYER")
        
    except Exception as e:
        print(f"Error in endfortheouche: {e}")


def create_player(name_p1, name_p2):
    print("Get or create player")
    global players_name_list

    # Utilise get_or_create pour chercher un joueur existant ou en créer un nouveau avec les valeurs par défaut
    print("Check player exist")
    if name_p1 in players_name_list:
        print(f"Player 1 {name_p1} exists")    
    else :
        print(f"Player 1 {name_p1} does not exists")  
        player1 = Player(
            name = name_p1, 
            total_match = 0, 
            total_win = 0, 
            p_win = 0,
            num_participated_tournaments = 0)
        player1.save()
        players_name_list.append(name_p1)
        print(f"Player {name_p1} creation done") 
    
    if name_p2 in players_name_list:
        print(f"Player 2 {name_p2} exists")    
    else :
        print(f"Player 2 {name_p2} does not exists")  
        player2 = Player(
            name = name_p2, 
            total_match = 0, 
            total_win = 0, 
            p_win = 0,
            num_participated_tournaments = 0)
        player2.save()
        players_name_list.append(name_p2)
        print(f"Player {name_p2} creation done") 
    
    #return player


def create_match(player1, player2, score_player1, score_player2, nbr_ball_touch_p1, nbr_ball_touch_p2, duration, is_tournoi, tournoi):
    print("MATCH BEING REGISTERD")
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
   
    
    print("MATCH SAVE IN DB")
    match.save()
    print("MATCH DONE")
    update_player_statistics(player1, match.winner, is_tournoi, tournoi)
    print("STAT P1 DONE")
    update_player_statistics(player2, match.winner, is_tournoi, tournoi)
    print("STAT P2 DONE") 

def update_player_statistics(player_name, winner, is_tournoi, tournoi):

    print("UPDATED DATA")
    global tournament_participations
    print("GET PLAYER")
    player = get_object_or_404(Player, name=player_name)
    print("PLAYER FIND")
 
    player.total_match += 1
    if winner == player.name :
        player.total_win += 1
    
    if player.total_match > 0:
        player.p_win = player.total_win / player.total_match

    if is_tournoi:
        if tournoi.name not in tournament_participations:
            tournament_participations[tournoi] = []
        
        if player_name not in tournament_participations[tournoi]:
            tournament_participations[tournoi].append(player.name)
            player.num_participated_tournaments += 1
        
    

    player.save()

def get_player_p_win(player_name):
    player = get_object_or_404(Player, name=player_name)
    return player.p_win

def create_tournament(name, nbr_player):
    print("tournoi created!!!")
    tournoi=Tournoi(name=name, nbr_player=nbr_player, winner="No one yet ...")
    tournoi.save()
    print(f"tournoi name : {tournoi.name}  *******!*!*!*!**!*!**!*!*!*!*!*!*!*!*!*")
    return tournoi

def update_tournament(name_tournoi, winner_name):
    tournoi = get_object_or_404(Tournoi, name=name_tournoi)
    
    print(f"in update tourna - tournoi name : {tournoi.name}  *******!*!*!*!**!*!**!*!*!*!*!*!*!*!*!*")
    

    tournoi.winner = winner_name
    print(f"in update tourna - TOURNOI winner is : {tournoi.winner}  *******!*!*!*!**!*!**!*!*!*!*!*!*!*!*!*")
    tournoi.save()


def getlen():
    return Tournoi.objects.count()
