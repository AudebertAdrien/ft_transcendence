# /pong/game/views.py

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
import json
import uuid

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


from .models import Match

def dashboards(request):
    # Fetches all Match objects from the database
    matches = Match.objects.all()
    # List of strings that will be used as the x-axis of the chart (using str.format() to convert match ids to strings)
    labels = ["Match {}".format(match.id) for match in matches]
    # List of data used as points for the chart (e.g. for bars, needed to be the same nbr of label strings and data)
    data = [match.score_player1 + match.score_player2 for match in matches]
    # Creates dictionary
    context = {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    }
    return render(request, 'dashboards.html', context)

