from django.db import models
from django.contrib.auth.models import User
from .turbo_game import TurboGame

class UserScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    game = models.ForeignKey(TurboGame, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
