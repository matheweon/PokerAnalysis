from algorithms.genetic_poker4 import Genome
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
    return matchups

matchups = generate_matchups()
raise_size = 3
bitsize = 6

def expected_value(match_num: int) -> float:
    return equities[(matchups[match_num][0], matchups[match_num][1])] / 50 - 1

def fitness(sb_genome: Genome, bb_genome: Genome) -> float:
    match_num = 0
    total_bb = 0
    while match_num < len(matchups):
        bb = 0
        # sb_actions:
        # 0: fold
        # 1: open, fold to 3bet
        # 2: open, call 3bet
        # 3: 4bet, fold to 5bet
        # 4: 4bet, call 5bet
        # 5: 6bet "all in"
        sb_action = sb_genome[card_dict[matchups[match_num][0][0]] * 13 + card_dict[matchups[match_num][0][1]]]
        # bb_actions:
        # 0: fold
        # 1: call open
        # 2: 3bet, fold to 4bet
        # 3: 3bet, call 4bet
        # 4: 5bet, fold to 6bet
        # 5: 5bet, call 6bet
        bb_action = bb_genome[card_dict[matchups[match_num][1][0]] * 13 + card_dict[matchups[match_num][1][1]]]

        if sb_action == 0: # SB folds
            bb -= 0.5
        else: # SB opens
            if bb_action == 0: # BB folds to open
                bb += 1
            elif bb_action == 1: # BB calls open
                bb += expected_value(match_num) * raise_size
            else: # BB 3bets
                if sb_action == 1: # SB folds to 3bet
                    bb -= raise_size
                elif sb_action == 2: # SB calls 3bet
                    bb += expected_value(match_num) * raise_size**2
                else: # SB 4bets
                    if bb_action == 2: # BB folds to 4bet
                        bb += raise_size**2
                    elif bb_action == 3: # BB calls 4bet
                        bb += expected_value(match_num) * raise_size**3
                    else: # BB 5bets
                        if sb_action == 3: # SB folds to 5bet
                            bb -= raise_size**3
                        elif sb_action == 4: # SB calls 5bet
                            bb += expected_value(match_num) * raise_size**4
                        else: # SB 6bets
                            if bb_action == 4: # BB folds to 6bet
                                bb += raise_size**4
                            else: # BB calls 6bet
                                bb += expected_value(match_num) * raise_size**5

        # Multiply EV by number of combos
        total_bb += bb * matchups[match_num][2]
        match_num += 1

    # Divides the total BBs by the total number of matchups analyzed, then multiplies by 100 to represent BB/100 hands
    total_bb = round(total_bb / (52*51*50*49/4) * 100, 4)
    return total_bb
