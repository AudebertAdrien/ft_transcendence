# /pong/game/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('check_user_exists/', views.check_user_exists, name='check_user_exists'),
    path('register_user/', views.register_user, name='register_user'),
    path('authenticate_user/', views.authenticate_user, name='authenticate_user'),
]
