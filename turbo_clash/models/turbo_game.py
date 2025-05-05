
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from turbo_clash.models.xon_token_balance import XonTokenBalance 

from django.utils import timezone

class TurboGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_flip = models.IntegerField(default=1)
    current_round = models.IntegerField(default=1)  # Track current round
    card_1 = models.ForeignKey('TurboCard', related_name='card_1', on_delete=models.SET_NULL, null=True, blank=True)
    card_2 = models.ForeignKey('TurboCard', related_name='card_2', on_delete=models.SET_NULL, null=True, blank=True)
    card_3 = models.ForeignKey('TurboCard', related_name='card_3', on_delete=models.SET_NULL, null=True, blank=True)
    card_4 = models.ForeignKey('TurboCard', related_name='card_4', on_delete=models.SET_NULL, null=True, blank=True)
    card_5 = models.ForeignKey('TurboCard', related_name='card_5', on_delete=models.SET_NULL, null=True, blank=True)
    card_6 = models.ForeignKey('TurboCard', related_name='card_6', on_delete=models.SET_NULL, null=True, blank=True)
    total_speed = models.IntegerField(default=0)
    round_played = models.IntegerField(default=0)
    flips_required = models.IntegerField(default=4)
    round_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    last_played = models.DateTimeField(null=True, blank=True)

    def calculate_total_speed(self):
        self.total_speed = sum([
            self.card_1.speed if self.card_1 else 0,
            self.card_2.speed if self.card_2 else 0,
            self.card_3.speed if self.card_3 else 0,
            self.card_4.speed if self.card_4 else 0,
            self.card_5.speed if self.card_5 else 0,
            self.card_6.speed if self.card_6 else 0,
        ])
        self.save()

    def reset_game(self):
        self.current_flip = 1
        self.total_speed = 0
        self.round_completed = False
        self.current_round = (self.current_round % 3) + 1  # Increment round number, loop back to 1 after 3
        self.last_played = timezone.now()
        self.save()

    def can_play(self):
        # if self.last_played is None:
        #     return True
        # return timezone.now() >= self.last_played + timezone.timedelta(hours=24)
        return True

    def update_xon_balance(self):
        try:
            xon_balance_entry = XonTokenBalance.objects.get(user=self.user)
        except XonTokenBalance.DoesNotExist:
            return 

        # Threshold to win or lose
        target_speed = 1000  # Player needs 1000 km/h to win

        # Check if player won or lost
        if self.total_speed >= target_speed:
            # Player wins: add 50% of wager to Xon balance
            xon_balance_entry.xon_balance += xon_balance_entry.xon_balance * Decimal('0.5')  # win 50%
        else:
            # Player loses: subtract 50% of wager from Xon balance
            xon_balance_entry.xon_balance -= xon_balance_entry.xon_balance * Decimal('0.4')  # lose 40%

        # Ensure Xon balance does not go negative
        if xon_balance_entry.xon_balance < 0:
            xon_balance_entry.xon_balance = 0
        
        # Save the updated balance
        xon_balance_entry.save()