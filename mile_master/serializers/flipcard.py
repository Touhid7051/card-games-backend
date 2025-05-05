from rest_framework import serializers

class FlipCardSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()