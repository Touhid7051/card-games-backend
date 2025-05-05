from django.urls import path
from .views import StartGameView, FlipCardView, GetUSDTBalanceView

urlpatterns = [
    path('start-game/', StartGameView.as_view(), name='start-game'),
    path('flip-card/<int:game_id>/', FlipCardView.as_view(), name='flip-card'),
    path('usdt-balance/', GetUSDTBalanceView.as_view(), name='usdt-balance'),
]
