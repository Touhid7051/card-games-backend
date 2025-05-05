
from django.utils import timezone
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from turbo_clash.models.turbo_game import TurboGame
from turbo_clash.models.turbo_card import TurboCard
from turbo_clash.models.xon_token_balance import XonTokenBalance
import random
from rest_framework import status

class TurboFlipCardView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        flip_count = request.data.get('flip_count')

        # Fetch or create the current TurboGame instance
        game, created = TurboGame.objects.get_or_create(user=user, round_completed=False)

        # Check if the user is starting a new set
        if created or game.round_completed:
            # If it's a new set, flip_count must be provided
            if flip_count not in [4, 6]:
                return Response({"error": "Invalid flip count. Must be 4 or 6."}, status=status.HTTP_400_BAD_REQUEST)

            # Initialize the game for a new set
            game.current_flip = 1
            game.flips_required = flip_count
            game.round_completed = False
            game.total_speed = 0
            game.round_played += 1  # Track the number of rounds played in the current set
            game.save()

        # Handle Xon Token balance validation
        try:
            xon_balance_entry = XonTokenBalance.objects.get(user=user)
        except XonTokenBalance.DoesNotExist:
            return Response({"error": "User does not have an Xon Token balance."}, status=400)

        if xon_balance_entry.xon_balance < 1:
            return Response({"error": "Not enough Xon Tokens to continue."}, status=400)

        # Select a random card
        card_ids = list(TurboCard.objects.values_list('id', flat=True))
        selected_card = TurboCard.objects.get(id=random.choice(card_ids))

        # Assign the card based on the current flip number
        if game.current_flip <= game.flips_required:
            setattr(game, f'card_{game.current_flip}', selected_card)

        # Calculate total speed for the game
        game.calculate_total_speed()

        # Increase the current flip count
        game.current_flip += 1

        # Check if round is completed
        if game.current_flip > game.flips_required:
            game.round_completed = True
            game.update_xon_balance()  # Update Xon Token balance after the round

        # Save the updated game state
        game.save()

        # Prepare the response
        response = {
            "card_name": selected_card.card_name,
            "card_speed": selected_card.speed,
            "current_total_speed": game.total_speed,
            "flip_number": game.current_flip - 1,
            "round_completed": game.round_completed,
            "remaining_flips": game.flips_required - (game.current_flip - 1)
        }

        if game.round_completed:
            response["message"] = "Round completed!"
            response["final_score"] = game.total_speed

        return Response(response)
