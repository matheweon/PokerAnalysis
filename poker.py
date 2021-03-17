from algorithms.genetic import Genome
from collections import namedtuple
import random
import copy

Card = namedtuple("Card", ["name", "rank", "suit"])

Hand = namedtuple("Hand", ["name", "card1", "card2"])

example = [
    Hand("AA", Card("As", 14, 3), Card("Ac", 14, 0)),
    Hand("72o", Card("7h", 7, 2), Card("2d", 2, 1)),
    Hand("JTs", Card("Jh", 11, 3), Card("Th", 10, 3))
]

full_deck = []
for suit in range(4):
    for rank in range(2, 15):
        name = ""
        name += ("x", "x", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")[rank]
        name += ("c", "d", "h", "s")[suit]
        full_deck.append(Card(name, rank, suit))

use_deck = []

def shuffle():
    global use_deck
    use_deck = copy.deepcopy(full_deck)
    random.shuffle(use_deck)

def generate_hand():
    card1 = use_deck.pop()
    card2 = use_deck.pop()
    if card1[1] == card2[1]:
        name = card1[0][0] + card2[0][0]
    else:
        if card1[1] > card2[1]:
            name = card1[0][0] + card2[0][0]
        else:
            name = card2[0][0] + card1[0][0]
        if card1[2] == card2[2]:
            name += "s"
        else:
            name += "o"
    return Hand(name, card1, card2)

'''def generate_hands(num: int) -> [Dice]:
    return [Hand(random.randint(1, 6), random.randint(1, 6)) for i in range(0, num)]'''

fitnesses = {}

def fitness(genome: Genome, num_hands: int) -> int:
    '''if genome["sb-fold"].values() in fitnesses:
        print("here")
        return fitnesses[genome["sb-fold"].values()]'''
    if genome["fitness"] != None:
        return genome["fitness"]

    chips = 100
    for i in range(num_hands):
        shuffle()
        #position = random.choice(["SB", "BB"])
        position = "SB"
        my_hand = generate_hand()
        op_hand = generate_hand()
        action = []
        if position == "SB":
            randomizer = random.randint(0, genome["sb-fold"][my_hand.name] + genome["sb-limp"][my_hand.name] + genome["sb-open"][my_hand.name])
            if randomizer < genome["sb-fold"][my_hand.name]:
                action += "fold"
            elif randomizer < genome["sb-fold"][my_hand.name] + genome["sb-limp"][my_hand.name]:
                action += "limp"
            else:
                action += "raise"
            # Opponent action here
            if action[0] == "fold":
                chips -= 0.5
            elif action[0] == "limp":
                # Opponent can only check when limped to
                if win_hand(my_hand, op_hand):
                    chips += 1
                else:
                    chips -= 1
            else:
                # Random opponent action
                action += random.choice(["fold", "call"])
                if action[1] == "fold":
                    chips += 1
                else:
                    if win_hand(my_hand, op_hand):
                        chips += 3
                    else:
                        chips -= 3
        else:
            # Opponent action here
            action += random.choice(["fold", "limp", "raise"])
            if action[0] == "fold":
                chips += 0.5
    #fitnesses[genome["sb-fold"].values()] = chips
    #print(fitnesses)
    genome["fitness"] = chips
    return chips
'''
9 - Royal Flush
8 - Straight Flush
7 - Four of a Kind
6 - Full House
5 - Flush
4 - Straight
3 - Three of a Kind
2 - Two Pairs
1 - One Pair
0 - High Card
'''
def win_hand(my_hand, op_hand):
    return random.choice([True, False])
    '''board = [use_deck.pop(), use_deck.pop(), use_deck.pop(), use_deck.pop(), use_deck.pop()]
    # Find flush
    for hand in [my_hand, op_hand]:
        suit_dict = {0: [], 1: [], 2: [], 3: []}
        for card in hand:
            suit_dict[card[1]] += card[0]
        for card in board:
            suit_dict[card[1]] += card[0]
        for suit in suit_dict:
            if len(suit_dict[suit]) >= 5:
                suit_dict[suit] = sorted(suit_dict[suit], reverse=True)[:5]
                hand[]'''
