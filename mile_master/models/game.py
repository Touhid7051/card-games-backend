from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from mile_master.models.mile_card import MileCard
from django.contrib import admin

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mile_master_games')
    current_flip = models.IntegerField(default=1)
    card_1 = models.ForeignKey(MileCard, related_name='card_1', on_delete=models.SET_NULL, null=True, blank=True)
    card_2 = models.ForeignKey(MileCard, related_name='card_2', on_delete=models.SET_NULL, null=True, blank=True)
    card_3 = models.ForeignKey(MileCard, related_name='card_3', on_delete=models.SET_NULL, null=True, blank=True)
    card_4 = models.ForeignKey(MileCard, related_name='card_4', on_delete=models.SET_NULL, null=True, blank=True)
    total_distance = models.IntegerField(default=0)
    round_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def calculate_total_distance(self):
        self.total_distance = sum([
            self.card_1.distance if self.card_1 else 0,
            self.card_2.distance if self.card_2 else 0,
            self.card_3.distance if self.card_3 else 0,
            self.card_4.distance if self.card_4 else 0,
        ])
        self.save()

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_distance','current_flip','round_completed', 'created_at')