from decimal import Decimal
from rest_framework import status, views
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Game, USDTBalance, PrizePool, CardFlip, GameResult
from .serializers import GameSerializer, CardFlipSerializer
from .utils import get_random_card, allocate_prize_pool, calculate_winnings
from django.db import transaction

class StartGameView(views.APIView):
    def post(self, request):
        user = request.user
        bet = Decimal(request.data.get('bet_amount', 0))

        print('bet',bet)
        
        usdt_balance = get_object_or_404(USDTBalance, user=user)

        if usdt_balance.balance < bet:
            return Response({'detail': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
        print('balance before',usdt_balance.balance)

        usdt_balance.balance -= bet
        usdt_balance.save()

        print('balance after',usdt_balance.balance)

        allocate_prize_pool(bet)

        game = Game.objects.create(user=user, total_bet=bet)
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FlipCardView(views.APIView):
    def post(self, request, game_id):
        game = get_object_or_404(Game, id=game_id, user=request.user)
        bet_amount = game.total_bet 

        if game.finished:
            return Response({'detail': 'Game already finished, no more flips allowed'}, status=status.HTTP_400_BAD_REQUEST)

        if game.cards_flipped >= 7:
            return Response({'detail': 'All 7 cards have been flipped. The game is over.'}, status=status.HTTP_400_BAD_REQUEST)

        # Flip a new card
        new_card = get_random_card()
        CardFlip.objects.create(game=game, card=new_card)

        if new_card == 'Legend':
            game.legend_count += 1
        elif new_card == 'Real Estate':
            game.real_estate_count += 1
        elif new_card == 'Land':
            game.land_count += 1
        elif new_card == 'Joker':
            game.joker_count += 1


        game.cards_flipped += 1
        if game.cards_flipped == 7:
            game.finished = True

            winning_category = calculate_winnings(game, bet_amount)

            if winning_category:
                GameResult.objects.create(
                    game=game,
                    user=request.user,
                    win_category=winning_category,
                )

        game.save()

        flipped_cards = CardFlip.objects.filter(game=game)
        serializer = CardFlipSerializer(flipped_cards, many=True)

        response_data = {
            'flipped_card': new_card,
            'cards_flipped': game.cards_flipped,
            'finished': game.finished,
            'all_flipped_cards': serializer.data
        }
        
        if game.finished:
            response_data['win_category'] = winning_category

        return Response(response_data, status=status.HTTP_200_OK)

class GetUSDTBalanceView(views.APIView):
    def get(self, request):
        balance = get_object_or_404(USDTBalance, user=request.user)
        return Response({'balance': balance.balance}, status=status.HTTP_200_OK)
