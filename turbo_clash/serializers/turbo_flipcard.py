from rest_framework import serializers

class TurboFlipCardSerializer(serializers.Serializer):
    flip_count = serializers.IntegerField()
