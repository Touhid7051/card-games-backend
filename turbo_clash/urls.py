# turbo_clash/urls.py

from django.urls import path
from turbo_clash.views.turbo_flipcard import TurboFlipCardView
from turbo_clash.views.turbo_user_history import TurboUserHistoryView

urlpatterns = [
    path('flip-cards/', TurboFlipCardView.as_view(), name='turbo-clash-flip-cards'),
    path('history/', TurboUserHistoryView.as_view(), name='turbo-clash-user-history'),
]
