from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import admin

class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)  # Sum of all round scores

    def update_total_score(self, score):
        self.total_score += score
        self.save()

    def __str__(self):
        return f"{self.user.username} - Total Score: {self.total_score}"

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_score')