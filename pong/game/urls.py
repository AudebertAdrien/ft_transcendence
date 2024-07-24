# /pong/game/urls.py

from django.urls import path
from . import views
from .views import player_list, tournoi_list, match_list

urlpatterns = [
    path('', views.index, name='index'),
    path('check_user_exists/', views.check_user_exists, name='check_user_exists'),
    path('register_user/', views.register_user, name='register_user'),
    path('authenticate_user/', views.authenticate_user, name='authenticate_user'),
    path('create_player/', views.create_player_view, name='create_player'),
    path('create_tournoi/', views.create_tournoi_view, name='create_tournoi'),
    path('create_match/', views.create_match_view, name='create_match'),
    path('players/', player_list, name='player_list'),
    path('matches/', match_list, name='match_list'),
    path('tournois/', tournoi_list, name='tournoi_list'),
]
