# /pong/game/models.py

from django.db import models
from django.contrib.auth.models import User

User.add_to_class('auth_token', models.CharField(max_length=100, null=True, blank=True, unique=True))