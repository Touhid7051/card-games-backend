from django.db import models
from django.contrib.auth.models import User

class USDTBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='legend_hunt_games')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

class PrizePool(models.Model):
    LEGEND = 'legend'
    REAL_ESTATE = 'real_estate'
    LAND = 'land'

    POOL_CHOICES = [
        (LEGEND, 'Legend Pool'),
        (REAL_ESTATE, 'Real Estate Pool'),
        (LAND, 'Land Pool')
    ]

    pool_name = models.CharField(max_length=50, choices=POOL_CHOICES, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    updated_at = models.DateTimeField(auto_now=True)


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_bet = models.DecimalField(max_digits=5, decimal_places=2)
    cards_flipped = models.IntegerField(default=0)
    legend_count = models.IntegerField(default=0)  # Count of Legend symbols flipped
    real_estate_count = models.IntegerField(default=0)  # Count of Real Estate symbols flipped
    land_count = models.IntegerField(default=0)  # Count of Land symbols flipped
    joker_count = models.IntegerField(default=0)  # Count of Joker symbols flipped
    created_at = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default=False)


class CardFlip(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    card = models.CharField(max_length=50) 
    flipped_at = models.DateTimeField(auto_now_add=True)

class GameResult(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    win_category = models.CharField(max_length=100)
    amount_won = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

