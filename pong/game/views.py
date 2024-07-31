# /pong/game/views.py

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

from django.core.exceptions import ObjectDoesNotExist
from .models import Player, Tournoi, Match
from .utils import create_player, create_tournoi, create_match
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
import json
import uuid


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            token = get_or_create_token(user)
            return JsonResponse({'registered': True, 'token': token})
        return JsonResponse({'registered': False, 'error': 'User already exists'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def check_user_exists(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'exists': True})
        return JsonResponse({'exists': False})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def authenticate_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username', '')
            password = data.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                token = get_or_create_token(user)
                return JsonResponse({'authenticated': True, 'token': token, 'user_id': user.id})
            else:
                return JsonResponse({'authenticated': False}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def get_or_create_token(user):
    if not user.auth_token:
        while True:
            token = str(uuid.uuid4())
            if not User.objects.filter(auth_token=token).exists():
                user.auth_token = token
                user.save()
                break
    return user.auth_token


####################### THEOUCHE PART ############################


@csrf_exempt
def create_player_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            
            # Vérifier que le nom est présent
            if not name:
                return JsonResponse({'error': 'Name is required'}, status=400)
            
            # Appeler la fonction create_player et traiter les exceptions
            player = create_player(
                name=name,
                total_match=data.get('total_match', 0),
                total_win=data.get('total_win', 0),
                p_win=data.get('p_win'),
                m_score_match=data.get('m_score_match'),
                m_score_adv_match=data.get('m_score_adv_match'),
                best_score=data.get('best_score', 0),
                m_nbr_ball_touch=data.get('m_nbr_ball_touch'),
                total_duration=data.get('total_duration'),
                m_duration=data.get('m_duration'),
                num_participated_tournaments=data.get('num_participated_tournaments', 0),
                num_won_tournaments=data.get('num_won_tournaments', 0)
            )
            return JsonResponse({'id': player.id, 'name': player.name})

        except ValueError as e:
            # Erreur spécifique à la validation
            return JsonResponse({'error': str(e)}, status=400)
        except json.JSONDecodeError:
            # Erreur de décodage JSON
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            # Erreur générale
            return JsonResponse({'error': 'An unexpected error occurred', 'details': str(e)}, status=500)

    # Méthode HTTP non supportée
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)



@csrf_exempt
def create_tournoi_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        nbr_player = data.get('nbr_player')
        date = data.get('date')
        winner_id = data.get('winner_id')
        if not (name and nbr_player and date):
            return JsonResponse({'error': 'Name, number of players, and date are required'}, status=400)
        
        winner = None
        if winner_id:
            try:
                winner = Player.objects.get(id=winner_id)
            except Player.DoesNotExist:
                return JsonResponse({'error': 'Winner not found'}, status=404)
        
        tournoi = create_tournoi(name, nbr_player, date, winner)
        return JsonResponse({
            'id': tournoi.id,
            'name': tournoi.name,
            'nbr_player': tournoi.nbr_player,
            'date': tournoi.date.isoformat(),
            'winner': winner.id if winner else None
        })
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

@csrf_exempt
def create_match_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        player1_id = data.get('player1_id')
        player2_id = data.get('player2_id')
        score_player1 = data.get('score_player1', 0)
        score_player2 = data.get('score_player2', 0)
        nbr_ball_touch_p1 = data.get('nbr_ball_touch_p1', 0)
        nbr_ball_touch_p2 = data.get('nbr_ball_touch_p2', 0)
        duration = data.get('duration')
        is_tournoi = data.get('is_tournoi', False)
        tournoi_id = data.get('tournoi_id')

        if not (player1_id and player2_id and duration):
            return JsonResponse({'error': 'Player IDs and duration are required'}, status=400)

        try:
            player1 = Player.objects.get(id=player1_id)
            player2 = Player.objects.get(id=player2_id)
        except Player.DoesNotExist:
            return JsonResponse({'error': 'One or both players not found'}, status=404)

        tournoi = None
        if tournoi_id:
            try:
                tournoi = Tournoi.objects.get(id=tournoi_id)
            except Tournoi.DoesNotExist:
                return JsonResponse({'error': 'Tournoi not found'}, status=404)

        match = create_match(player1, player2, score_player1, score_player2, nbr_ball_touch_p1, nbr_ball_touch_p2, duration, is_tournoi, tournoi)
        return JsonResponse({
            'id': match.id,
            'player1': match.player1.id,
            'player2': match.player2.id,
            'score_player1': match.score_player1,
            'score_player2': match.score_player2,
            'nbr_ball_touch_p1': match.nbr_ball_touch_p1,
            'nbr_ball_touch_p2': match.nbr_ball_touch_p2,
            'duration': str(match.duration),
            'is_tournoi': match.is_tournoi,
            'tournoi': match.tournoi.id if match.tournoi else None
        })
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


def player_list(request):
    players = Player.objects.all()
    return render(request, 'pong/player_list.html', {'players': players})

def match_list(request):
    matches = Match.objects.select_related('player1', 'player2', 'winner', 'tournoi').all()
    return render(request, 'pong/match_list.html', {'matches': matches})

def tournoi_list(request):
    tournois = Tournoi.objects.select_related('winner').all()
    return render(request, 'pong/tournoi_list.html', {'tournois': tournois})

####################### THEOUCHE PART ############################
