from decimal import Decimal
import random
from .models import PrizePool

# def get_random_card():
#     """Returns a random card from the available 48 cards."""
#     cards = ['Legend', 'Real Estate', 'Land', 'Joker']
#     return random.choice(cards)

# Create the full deck of 48 cards
def create_deck():
    deck = (
        ['Legend'] * 8 +
        ['Real Estate'] * 8 +
        ['Land'] * 8 +
        ['Joker'] * 5 +
        ['Blank'] * 19
    )
    random.shuffle(deck)
    return deck

# Get a single random card
def get_random_card():
    """Draws one card from the shuffled deck."""
    deck = create_deck()
    return deck.pop() if deck else None


def allocate_prize_pool(bet):
    bet = Decimal(bet)
    
    if bet == Decimal('5.00'):
        legend_pool = PrizePool.objects.get(pool_name='legend')
        legend_pool.amount += bet
        legend_pool.save()
    elif bet == Decimal('7.50'):
        legend_pool = PrizePool.objects.get(pool_name='legend')
        legend_pool.amount += Decimal('5.00')
        legend_pool.save()
        
        real_estate_pool = PrizePool.objects.get(pool_name='real_estate')
        real_estate_pool.amount += Decimal('2.50')
        real_estate_pool.save()
    elif bet == Decimal('10.00'):
        legend_pool = PrizePool.objects.get(pool_name='legend')
        legend_pool.amount += Decimal('5.00')
        legend_pool.save()
        
        real_estate_pool = PrizePool.objects.get(pool_name='real_estate')
        real_estate_pool.amount += Decimal('2.50')
        real_estate_pool.save()
        
        land_pool = PrizePool.objects.get(pool_name='land')
        land_pool.amount += Decimal('2.50')
        land_pool.save()


def calculate_winnings(game, bet_amount):
    winning_category = None

    if bet_amount == Decimal('5.00'): 
        if game.legend_count == 6 and game.joker_count >= 1:
            winning_category = 'Epic Victory'
        elif game.legend_count == 6:
            winning_category = 'Legendary Set'
        elif game.legend_count == 5 and game.joker_count >= 1:
            winning_category = 'Heroic Win'
        elif game.legend_count == 4 and game.joker_count >= 1:
            winning_category = 'Adventurer’s Reward'
        elif game.legend_count == 3 and game.joker_count >= 1:
            winning_category = 'Explorer’s Prize'

    elif bet_amount == Decimal('7.50'): 
        if game.real_estate_count == 6 and game.joker_count >= 1:
            winning_category = 'Epic Victory (Real Estate)'
        elif game.real_estate_count == 6:
            winning_category = 'Legendary Set (Real Estate)'
        elif game.real_estate_count == 5 and game.joker_count >= 1:
            winning_category = 'Heroic Win (Real Estate)'
        elif game.real_estate_count == 4 and game.joker_count >= 1:
            winning_category = 'Adventurer’s Reward (Real Estate)'
        elif game.real_estate_count == 3 and game.joker_count >= 1:
            winning_category = 'Explorer’s Prize (Real Estate)'

        if game.legend_count == 6 and game.joker_count >= 1:
            winning_category = winning_category or 'Epic Victory'
        elif game.legend_count == 6:
            winning_category = winning_category or 'Legendary Set'
        elif game.legend_count == 5 and game.joker_count >= 1:
            winning_category = winning_category or 'Heroic Win'
        elif game.legend_count == 4 and game.joker_count >= 1:
            winning_category = winning_category or 'Adventurer’s Reward'
        elif game.legend_count == 3 and game.joker_count >= 1:
            winning_category = winning_category or 'Explorer’s Prize'

    elif bet_amount == Decimal('10.00'):
        if game.land_count == 6 and game.joker_count >= 1:
            winning_category = 'Epic Victory (Land)'
        elif game.land_count == 6:
            winning_category = 'Legendary Set (Land)'
        elif game.land_count == 5 and game.joker_count >= 1:
            winning_category = 'Heroic Win (Land)'
        elif game.land_count == 4 and game.joker_count >= 1:
            winning_category = 'Adventurer’s Reward (Land)'
        elif game.land_count == 3 and game.joker_count >= 1:
            winning_category = 'Explorer’s Prize (Land)'

        if game.legend_count == 6 and game.joker_count >= 1:
            winning_category = winning_category or 'Epic Victory'
        elif game.legend_count == 6:
            winning_category = winning_category or 'Legendary Set'
        elif game.legend_count == 5 and game.joker_count >= 1:
            winning_category = winning_category or 'Heroic Win'
        elif game.legend_count == 4 and game.joker_count >= 1:
            winning_category = winning_category or 'Adventurer’s Reward'
        elif game.legend_count == 3 and game.joker_count >= 1:
            winning_category = winning_category or 'Explorer’s Prize'

        if game.real_estate_count == 6 and game.joker_count >= 1:
            winning_category = winning_category or 'Epic Victory (Real Estate)'
        elif game.real_estate_count == 6:
            winning_category = winning_category or 'Legendary Set (Real Estate)'
        elif game.real_estate_count == 5 and game.joker_count >= 1:
            winning_category = winning_category or 'Heroic Win (Real Estate)'
        elif game.real_estate_count == 4 and game.joker_count >= 1:
            winning_category = winning_category or 'Adventurer’s Reward (Real Estate)'
        elif game.real_estate_count == 3 and game.joker_count >= 1:
            winning_category = winning_category or 'Explorer’s Prize (Real Estate)'

    return winning_category
