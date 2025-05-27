import random

def dealer_play(dealer_cards):
    while calculate_points(dealer_cards) < 17:
        dealer_cards.append(draw_card())
    return dealer_cards

def draw_card():
    return random.choice(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'])

def calculate_points(cards):
    points = 0
    ace_count = 0
    for card in cards:
        if card in ['J', 'Q', 'K']:
            points += 10
        elif card == 'A':
            ace_count += 1
            points += 11
        else:
            points += int(card)
    while points > 21 and ace_count:
        points -= 10
        ace_count -= 1
    return points
