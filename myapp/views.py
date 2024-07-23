# myapp/views.py

from django.shortcuts import render, get_object_or_404
from .models import Player, Match, Tournoi
from django.http import JsonResponse
from django.db.models import Max

def player_statistics(request, player_name):
    player = get_object_or_404(Player, nam = player_name)

    #filtre on tab
    matches_as_player1 = Match.objects.filter(player1=player)
    matches_as_player2 = Match.objects.filter(player2=player)
    won_matches = Match.objects.filter(winner=player)
    part_tourn_as_p1 = Tournoi.objects.filter(matches__is_tournoi=True, matches__player1=player)
    part_tourn_as_p2 = Tournoi.objects.filter(matches__is_tournoi=True, matches__player2=player)
    won_tourn = Tournoi.objects.filter(winner=player)

    # calulate stat
    total_match = match_as_player1.count() + match_as_player2.count()
    total_score = sum([match.score_player1 for match in matches_as_player1 ]) + sum([match.score_player2 for match in matches_as_player2])
    total_score_adv = sum([match.score_player2 for match in matches_as_player1 ]) + sum([match.score_player1 for match in matches_as_player2])
    total_win =  won_matches.count()
    p_win = (total_win / total_match) * 100
    m_score_match = total_score / total_match
    m_score_adv_match = total_score_adv / total_match
    nbr_ball_touch = sum([match.nbr_ball_touch_p1 for match in matches_as_player1]) + sum([match.nbr_ball_touch_p2 for match in matches_as_player2])
    m_nbr_ball_touch = nbr_ball_touch / total_match
    total_duration = sum([match.duration for match in matches_as_player1]) + sum(match.duration for match in matches_as_player2)
    m_duration = total_duration / total_match
    total_tourn_p = part_tourn_as_p1.count() + part_tourn_as_p2.count()
    total_win_tourn = won_tourn.count()
    p_win_tourn = (total_win_tourn / total_tourn_p) * 100

    best_score_as_player1 = matches_as_player1.aggregate(Max('score_player1'))['score_player1__max']
    best_score_as_player2 = matches_as_player2.aggregate(Max('score_player2'))['score_player2__max']
    best_score = max(best_score_as_player1, best_score_as_player2)

    data = {
        'player_name': player.name,
        'number of match played' : total_match
        'number of win (matches)' : total_win
        'pourcentage of victory' : p_win
        'num_participated_tournaments': num_participated_tournaments,
        'num_won_tournaments': num_won_tournaments
    }


    

