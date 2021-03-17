from algorithms.genetic_poker2 import Genome
from collections import namedtuple
from equities2 import equities
import random
import copy

Card = namedtuple("Card", ["name", "rank", "suit"])
Matchup = namedtuple("Matchup", ["my_hand", "op_hand", "combos"])

matchups_example = [
    Matchup("AK", "QQ", 24),
    Matchup("27", "AA", 72),
    Matchup("Q5", "5Q", 24)
]

card_dict = {
    "A": 0,
    "K": 1,
    "Q": 2,
    "J": 3,
    "T": 4,
    "9": 5,
    "8": 6,
    "7": 7,
    "6": 8,
    "5": 9,
    "4": 10,
    "3": 11,
    "2": 12
}

cards = ("x", "x", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
suits = ("c", "d", "h", "s")

full_deck = []
for suit in range(4):
    for rank in range(2, 15):
        name = ""
        name += cards[rank]
        name += suits[suit]
        full_deck.append(Card(name, rank, suits[suit]))

use_deck = []

def generate_matchups(num: int) -> [Matchup]:
    matchups = []
    '''for i in range(52):
        for j in range(52):
            if j == i:
                break
            for k in range(52):
                if k == i or k == j:
                    break
                for l in range(52):
                    if l == i or l == j or l == k:
                        break
                    use_deck = copy.deepcopy(full_deck)
                    my_card1 = use_deck[i]
                    my_card2 = use_deck[j]
                    my_hand = ""
                    if my_card1[1] == my_card2[1]: # Pocket Pair
                        my_hand = my_card1[0][0] + my_card2[0][0]
                    elif my_card1[2] == my_card2[2]: # Suited
                        if my_card1[1] > my_card2[1]:
                            my_hand = my_card1[0][0] + my_card2[0][0]
                        else:
                            my_hand = my_card2[0][0] + my_card1[0][0]
                    else: # Unsuited
                        if my_card1[1] < my_card2[1]:
                            my_hand = my_card1[0][0] + my_card2[0][0]
                        else:
                            my_hand = my_card2[0][0] + my_card1[0][0]
                    op_card1 = use_deck[k]
                    op_card2 = use_deck[l]
                    op_hand = ""
                    if op_card1[1] == op_card2[1]: # Pocket Pair
                        op_hand = op_card1[0][0] + op_card2[0][0]
                    elif op_card1[2] == op_card2[2]: # Suited
                        if op_card1[1] > op_card2[1]:
                            op_hand = op_card1[0][0] + op_card2[0][0]
                        else:
                            op_hand = op_card2[0][0] + op_card1[0][0]
                    else: # Unsuited
                        if op_card1[1] < op_card2[1]:
                            op_hand = op_card1[0][0] + op_card2[0][0]
                        else:
                            op_hand = op_card2[0][0] + op_card1[0][0]
                    new = True
                    for matchup_id in range(len(matchups)):
                        if matchups[matchup_id][0] == my_hand and matchups[matchup_id][1] == op_hand:
                            matchups.append(Matchup(my_hand, op_hand, matchups[matchup_id][2] + 1))
                            new = False
                            del matchups[matchup_id]
                            print(len(matchups))
                            print(matchups[-1])
                            break
                    if new:
                        matchups.append(Matchup(my_hand, op_hand, 1))'''
    for rank1 in range(2, 15):
        for rank2 in range(2, 15):
            for rank3 in range(2, 15):
                for rank4 in range(2, 15):
                    if rank1 == rank2: # Pocket Pair
                        if rank3 == rank4: # vs Pocket Pair
                            if rank1 == rank3: # vs Same Hand
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 6))
                            else:
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 36))
                        elif rank3 > rank4: # vs Suited
                            if rank1 == rank3 or rank1 == rank4: # Shares Card
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 12))
                            else:
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 24))
                        elif rank3 < rank4: # vs Unsuited
                            if rank1 == rank3 or rank1 == rank4: # Shares Card
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 36))
                            else:
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 72))
                    elif rank1 > rank2: # Suited
                        if rank3 == rank4: # vs Pocket Pair
                            if rank1 == rank3 or rank2 == rank3: # Shares Card
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 12))
                            else:
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 24))
                        elif rank3 > rank4: # vs Suited
                            if rank1 == rank3 and rank2 == rank4: # Shares Both Cards
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 12))
                            elif rank1 == rank3 or rank1 == rank4 or rank2 == rank3 or rank2 == rank4: # Shares Card
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 12))
                            else:
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 16))
                        elif rank3 < rank4: # vs Unsuited
                            if rank1 == rank4 and rank2 == rank3: # Shares Both Cards
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 24))
                            elif rank1 == rank3 or rank1 == rank4 or rank2 == rank3 or rank2 == rank4: # Shares Card
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 36))
                            else:
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 48))
                    elif rank1 < rank2: # Unsuited
                        if rank3 == rank4: # vs Pocket Pair
                            if rank1 == rank3 or rank2 == rank3: # Shares Card
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 36))
                            else:
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 72))
                        elif rank3 > rank4: # vs Suited
                            if rank1 == rank4 and rank2 == rank3: # Shares Both Cards
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 24))
                            elif rank1 == rank3 or rank1 == rank4 or rank2 == rank3 or rank2 == rank4: # Shares Card
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 36))
                            else:
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 48))
                        elif rank3 < rank4: # vs Unsuited
                            if rank1 == rank3 and rank2 == rank4: # Shares Both Cards
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 84))
                            elif rank1 == rank3 or rank1 == rank4 or rank2 == rank3 or rank2 == rank4: # Shares Card
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 108))
                            else:
                                matchups.append(Matchup(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4], 144))
    combos = 0
    for matchup in matchups:
        combos += matchup[2]
    #print("matchups:", len(matchups))
    #print("combos:", combos)
    return matchups


stack_size = 100
fitnesses = {}
def fitness(genome: Genome, matchups: [Matchup], op_genome: Genome) -> float:
    '''if ''.join(str(g) for g in genome) in fitnesses:
        #print(len(fitnesses))
        return fitnesses[''.join(str(g) for g in genome)]'''
    match_num = 0
    total_bb = 0
    while match_num < len(matchups):
        bb = 0
        #if match_num % 2 == 0: # Small Blind
        if genome[card_dict[matchups[match_num][0][0]] * 13 + card_dict[matchups[match_num][0][1]]] == 1: # All in
            if op_genome[169 + card_dict[matchups[match_num][1][0]] * 13 + card_dict[matchups[match_num][1][1]]] == 1: # Opponent calls
                bb += (equities[(matchups[match_num][0], matchups[match_num][1])] / 50 - 1) * stack_size
            else: # Opponent folds
                bb += 1
        else: # Fold
            bb -= 0.5
        #else: # Big Blind
        if op_genome[card_dict[matchups[match_num][1][0]] * 13 + card_dict[matchups[match_num][1][1]]] == 1: # Opponent goes all in
            if genome[169 + card_dict[matchups[match_num][0][0]] * 13 + card_dict[matchups[match_num][0][1]]] == 1: # Call
                bb += (equities[(matchups[match_num][0], matchups[match_num][1])] / 50 - 1) * stack_size
            else: # Fold
                bb -= 1
        else: # Opponent folds
            bb += 0.5
        total_bb += bb * matchups[match_num][2] # Multiply EV by number of combos
        match_num += 1
    total_bb = round(total_bb, 2)
    '''fitnesses[''.join(str(g) for g in genome)] = total_bb'''
    return total_bb

'''def from_genome(genome: Genome, things: [Thing]) -> [Thing]:
    result = []
    for i, thing in enumerate(things):
        if genome[i] == 1:
            result += [thing]

    return result


def to_string(things: [Thing]):
    return f"[{', '.join([t.name for t in things])}]"


def value(things: [Thing]):
    return sum([t.value for t in things])


def weight(things: [Thing]):
    return sum([p.weight for p in things])


def print_stats(things: [Thing]):
    print(f"Things: {to_string(things)}")
    print(f"Value {value(things)}")
    print(f"Weight: {weight(things)}")'''
