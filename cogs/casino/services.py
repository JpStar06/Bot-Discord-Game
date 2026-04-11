from database import get_connection
import random

def spin_slots(aposta: int):
    EMOJIS = ["🍒", "🍋", "🍉", "⭐", "💎", "💶", "🪙"]
    r1 = random.choice(EMOJIS)
    r2 = random.choice(EMOJIS)
    r3 = random.choice(EMOJIS)

    if r1 == r2 == r3:
        return (r1, r2, r3), aposta * 6, "jackpot"
    elif r1 == r2 or r2 == r3 or r1 == r3:
        return (r1, r2, r3), aposta * 3, "win"
    else:
        return (r1, r2, r3), -aposta, "lose"
    

def draw_card():
    deck = [2,3,4,5,6,7,8,9,10,10,10,10,11]
    return random.choice(deck)

def calculate_hand(hand):
    total = sum(hand)

    # tratar Ás
    while total > 21 and 11 in hand:
        hand[hand.index(11)] = 1
        total = sum(hand)

    return total

def start_game():
    player = [draw_card(), draw_card()]
    dealer = [draw_card(), draw_card()]

    return player, dealer