from rest_framework import serializers
from .models import Game, CardFlip, GameResult

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'user', 'total_bet', 'cards_flipped', 'finished', 'created_at']

class CardFlipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardFlip
        fields = ['card', 'flipped_at']

class GameResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameResult
        fields = ['game', 'user', 'win_category', 'amount_won', 'created_at']
