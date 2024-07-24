from .models import Player, Tournoi, Match
from django.core.exceptions import ValidationError

def create_player(
    name, 
    total_match=0, 
    total_win=0, 
    p_win= None, 
    m_score_match= None, 
    m_score_adv_match= None, 
    best_score=0, 
    m_nbr_ball_touch= None, 
    total_duration= None, 
    m_duration= None, 
    num_participated_tournaments=0, 
    num_won_tournaments=0
):
    if Player.objects.filter(name=name).exists():
        raise ValueError(f"A player with the name '{name}' already exists.")

    player = Player(
        name=name,
        total_match  = total_match,
        total_win = total_win,
        p_win = p_win,
        m_score_match = m_score_match,
        m_score_adv_match = m_score_adv_match,
        best_score = best_score,
        m_nbr_ball_touch = m_nbr_ball_touch,
        total_duration = total_duration,
        m_duration = m_duration,
        num_participated_tournaments = num_participated_tournaments,
        num_won_tournaments = num_won_tournaments
    )
    player.save()
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

""" def complete_match(match_id, score_player1, score_player2, nbr_ball_touch_p1, nbr_ball_touch_p2, duration):
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
    return match """

""" def complete_tournoi(tournoi_id, player):
    try:
        tournoi = Tournoi.objects.get(id = tournoi_id)
    except Tournoi.DoesNotExist:
        raise ValidationError(f"Tournoi with id {tournoi_id} does not exist")
    
    tournoi.winner = player
    tournoi.save()
    return tournoi """

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
        'number of match played' : total_match,
        'number of win (matches)' : total_win,
        'pourcentage of victory' : p_win,
        'mean score per match' : m_score_match,
        'mean score adv per match' : m_score_adv_match,
        'best score' : best_score,
        'mean nbr ball touch' : m_nbr_ball_touch,
        'total duration played' : total_duration,
        'mean duration per match' : m_duration,
        'num_participated_tournaments': num_participated_tournaments,
        'num_won_tournaments': num_won_tournaments
    }

    return data


    

