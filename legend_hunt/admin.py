from django.contrib import admin
from .models import USDTBalance, PrizePool, Game, CardFlip, GameResult

# Register the models
@admin.register(USDTBalance)
class USDTBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'updated_at')
    search_fields = ('user__username',)

@admin.register(PrizePool)
class PrizePoolAdmin(admin.ModelAdmin):
    list_display = ('pool_name', 'amount', 'updated_at')
    search_fields = ('pool_name',)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_bet', 'cards_flipped', 'finished', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('finished', 'created_at')

@admin.register(CardFlip)
class CardFlipAdmin(admin.ModelAdmin):
    list_display = ('game', 'card', 'flipped_at')
    search_fields = ('game__user__username', 'card')
    list_filter = ('flipped_at',)

@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = ('game', 'user')