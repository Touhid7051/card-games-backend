from rest_framework import serializers

class TurboUserHistorySerializer(serializers.Serializer):
    game_id = serializers.IntegerField()
    score = serializers.IntegerField()
    played_at = serializers.DateTimeField()
