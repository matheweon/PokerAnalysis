from algorithms.genetic_poker3 import Genome
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

inv_card_dict = {v: k for k, v in card_dict.items()}

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

def generate_matchups() -> [Matchup]:
    matchups = []
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

matchups = generate_matchups()
stack_size = 200
bitsize = 5
fitnesses = {}
def fitness(sb_genome: Genome, bb_genome: Genome) -> float:
    '''if ''.join(str(g) for g in genome) in fitnesses:
        #print(len(fitnesses))
        return fitnesses[''.join(str(g) for g in genome)]'''
    match_num = 0
    total_bb = 0
    while match_num < len(matchups):
        bb = 0
        jam_freq = sb_genome[card_dict[matchups[match_num][0][0]] * 13 + card_dict[matchups[match_num][0][1]]]
        call_freq = bb_genome[card_dict[matchups[match_num][1][0]] * 13 + card_dict[matchups[match_num][1][1]]]
        if jam_freq >= 1: # SB all in
            if call_freq >= 1: # BB calls
                bb += (equities[(matchups[match_num][0], matchups[match_num][1])] / 50 - 1) * stack_size * jam_freq * call_freq
            bb += 1 * jam_freq * (bitsize - call_freq - 1) # BB folds
        bb -= 0.5 * (bitsize - jam_freq - 1) # SB folds
        total_bb += bb * matchups[match_num][2] / (bitsize - 1)**2 # Multiply EV by number of combos and divide by total frequency
        match_num += 1
    total_bb = round(total_bb / (52*51*50*49/4) * 100, 4)
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
