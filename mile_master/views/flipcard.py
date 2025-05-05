from rest_framework import serializers, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from mile_master.models.game import Game
from mile_master.models.mile_card import MileCard
from mile_master.models.leaderboard import Leaderboard
import random


class FlipCardView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        game, created = Game.objects.get_or_create(user=user, round_completed=False)

        # Select a random card
        card_ids = list(MileCard.objects.values_list('id', flat=True))
        selected_card = MileCard.objects.get(id=random.choice(card_ids))

        # Assign the card based on current flip number
        if game.current_flip == 1:
            game.card_1 = selected_card
        elif game.current_flip == 2:
            game.card_2 = selected_card
        elif game.current_flip == 3:
            game.card_3 = selected_card
        elif game.current_flip == 4:
            game.card_4 = selected_card
            game.round_completed = True 

        # Calculate total distance for the game
        game.calculate_total_distance()

        # Increase the current flip count
        game.current_flip += 1
        game.save()

        response = {
            "card_name": selected_card.card_name,
            "card_distance": selected_card.distance,
            "current_total_distance": game.total_distance,
            "flip_number": game.current_flip - 1
        }

        # If the round is completed, update the leaderboard
        if game.round_completed:
            leaderboard, created = Leaderboard.objects.get_or_create(user=user)
            leaderboard.update_total_score(game.total_distance)  # Now update the total score
            response["message"] = "Round completed!"
            response["final_score"] = game.total_distance

        return Response(response)
