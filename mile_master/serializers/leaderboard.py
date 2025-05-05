from rest_framework import serializers
from mile_master.models.leaderboard import Leaderboard

class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = ['user', 'highest_score']