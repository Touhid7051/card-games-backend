from django.urls import path
from .views.flipcard import FlipCardView
from .views.leaderboard import LeaderboardView

urlpatterns = [
    path('flip-cards/', FlipCardView.as_view(), name='mile-master-flip-cards'),
    path('leaderboard/', LeaderboardView.as_view(), name='mile-master-player-rank'),
]