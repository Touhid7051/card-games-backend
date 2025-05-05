# turbo_clash/models/turbo_card.py

from django.db import models

class TurboCard(models.Model):
    speed = models.IntegerField()
    card_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.card_name} - {self.speed} km/h"
