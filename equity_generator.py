from collections import namedtuple
import random
import copy

# 10000 trials: 3 seconds per trial
# Total evaluations: 169*168/2 = 14196
# 3 * 14196 = 42588 seconds = 709.8 minutes = 11.83 hours
# 10000 trials ~= 12 hours but is only accurate to about within +-1%
limit = 50000
precision = 6

Card = namedtuple("Card", ["name", "rank", "suit"])
Hand = namedtuple("Hand", ["name", "card1", "card2", "type"])

#txt = open("equities.txt", "w")
#csv = open("equities.csv", "w")
py = open("equities.py", "w")
py.write("equities = {\n")
equities = {}

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

hands = {}
for rank1 in range(2, 15):
    for rank2 in range(2, 15):
        card1 = cards[rank1]
        card2 = cards[rank2]
        name = card1 + card2
        hands[name] = []
        if rank1 == rank2: # Pocket Pair
            for suit_id in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)):
                hands[name].append(Hand(name, Card(card1 + suits[suit_id[0]], rank1, suits[suit_id[0]]), Card(card2 + suits[suit_id[1]], rank2, suits[suit_id[1]]), "p"))
        elif rank1 > rank2: # Suited
            for suit_id in range(4):
                hands[name].append(Hand(name, Card(card1 + suits[suit_id], rank1, suits[suit_id]), Card(card2 + suits[suit_id], rank2, suits[suit_id]), "s"))
        else: # Unsuited
            for suit_id in ((0, 1), (0, 2), (0, 3), (1, 0), (1, 2), (1, 3), (2, 0), (2, 1), (2, 3), (3, 0), (3, 1), (3, 2)):
                hands[name].append(Hand(name, Card(card1 + suits[suit_id[0]], rank1, suits[suit_id[0]]), Card(card2 + suits[suit_id[1]], rank2, suits[suit_id[1]]), "o"))

def find_flush(board):
    suit_count = {
        "c": [],
        "d": [],
        "h": [],
        "s": []
    }
    for card in board:
        suit_count[card[2]].append(card[1])
    for suit in suit_count:
        if len(suit_count[suit]) >= 5:
            straight_flush = find_straight_helper(suit_count[suit])
            if straight_flush > 0:
                return [8, straight_flush] # Straight Flush
            else:
                return [5] + sorted(suit_count[suit], reverse=True)[:5] # Flush
    return [0]

def find_straight_helper(ranks):
    if 14 in ranks and 2 in ranks and 3 in ranks and 4 in ranks and 5 in ranks:
        return 5
    for i in range(6, 15):
        if set([i-4, i-3, i-2, i-1, i]).issubset(ranks):
            return i
    return 0

def find_straight(ranking, board):
    if ranking[0] > 4:
        return ranking # Return if better than straight
    ranks = []
    for card in board:
        if card[1] not in ranks:
            ranks.append(card[1])
    straight = find_straight_helper(ranks)
    if straight > 0:
        return [4, straight] # Straight
    else:
        return ranking

def find_pairs(ranking, board):
    if ranking[0] > 7:
        return ranking # Return if straight flush
    pair_count = {
        1: [],
        2: [],
        3: [],
        4: []
    }
    for card in board:
        if card[1] in pair_count[3]:
            pair_count[3].remove(card[1])
            pair_count[4].append(card[1])
        elif card[1] in pair_count[2]:
            pair_count[2].remove(card[1])
            pair_count[3].append(card[1])
        elif card[1] in pair_count[1]:
            pair_count[1].remove(card[1])
            pair_count[2].append(card[1])
        else:
            pair_count[1].append(card[1])
    if len(pair_count[4]) == 1:
        kicker = sorted(pair_count[4], reverse=True)[0]
        return [7, pair_count[4][0], kicker] # Four Of A Kind
    elif len(pair_count[3]) == 1 and len(pair_count[2]) >= 1:
        pair = sorted(pair_count[2], reverse=True)[0]
        return [6, pair_count[3][0], pair] # Full House
    elif ranking[0] > 3:
        return ranking # Return if better than trips
    elif len(pair_count[3]) == 2:
        trips = sorted(pair_count[3], reverse=True)
        kickers = sorted((pair_count[1] + [trips[1]]), reverse=True)
        return [3, trips[0], kickers[0], kickers[1]] # Three Of A Kind (with two trips)
    elif len(pair_count[3]) == 1:
        kicker1 = sorted(pair_count[1], reverse=True)[0]
        kicker2 = sorted(pair_count[1], reverse=True)[1]
        return [3, pair_count[3][0], kicker1, kicker2] # Three Of A Kind
    elif len(pair_count[2]) == 3:
        pairs = sorted(pair_count[2], reverse=True)
        kicker = sorted((pair_count[1] + [pairs[2]]), reverse=True)[0]
        return [2, pairs[0], pairs[1], kicker] # Two Pair (with three pairs)
    elif len(pair_count[2]) == 2:
        pairs = sorted(pair_count[2], reverse=True)
        kicker = sorted(pair_count[1], reverse=True)[0]
        return [2, pairs[0], pairs[1], kicker] # Two Pair
    elif len(pair_count[2]) == 1:
        kickers = sorted(pair_count[1], reverse=True)
        return [1, pair_count[2][0], kickers[0], kickers[1], kickers[2]] # One Pair
    else:
        kickers = sorted(pair_count[1], reverse=True)
        return [0, kickers[0], kickers[1], kickers[2], kickers[3], kickers[4]]

for hands1 in hands:
    for hands2 in hands:
        if hands1 == hands2:
            equity = str(round(50, precision))
            equities[(hands1[0], hands2[0])] = equity
            print("hand1:", hands1, " hand2:", hands2)
            print("equity:", equity)
            py.write("\t(\"" + hands1 + "\", \"" + hands2 + "\"): " + equity + ",\n")
        elif ((hands1, hands2) not in equities):
            matchups = []
            matches = 0
            wins = 0
            ties = 0
            losses = 0
            for hand1 in hands[hands1]:
                for hand2 in hands[hands2]:
                    if not (hand1[1] == hand2[1] or hand1[1] == hand2[2] or hand1[2] == hand2[1] or hand1[2] == hand2[2]):
                        matchups.append((hand1, hand2))
            while matches < limit:
                matches += 1
                matchup = random.choice(matchups)
                use_deck = copy.deepcopy(full_deck)
                use_deck.remove(matchup[0][1])
                use_deck.remove(matchup[0][2])
                use_deck.remove(matchup[1][1])
                use_deck.remove(matchup[1][2])
                board = []
                board.append(use_deck.pop(random.randrange(len(use_deck))))
                board.append(use_deck.pop(random.randrange(len(use_deck))))
                board.append(use_deck.pop(random.randrange(len(use_deck))))
                board.append(use_deck.pop(random.randrange(len(use_deck))))
                board.append(use_deck.pop(random.randrange(len(use_deck))))
                board1 = board + [matchup[0][1], matchup[0][2]]
                board2 = board + [matchup[1][1], matchup[1][2]]
                ranking1 = [0]
                ranking2 = [0]
                '''
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
                ranking1 = find_flush(board1)
                ranking2 = find_flush(board2)
                if ranking1[0] == 8:
                    if ranking2[0] == 8:
                        if ranking1[1] == ranking2[1]:
                            ties += 1
                            continue
                        elif ranking1[1] > ranking2[1]:
                            wins += 1
                            continue
                        else:
                            losses += 1
                            continue
                    else:
                        wins += 1
                        continue
                elif ranking2[0] == 8:
                    losses += 1
                    continue

                ranking1 = find_straight(ranking1, board1)
                ranking2 = find_straight(ranking2, board2)
                ranking1 = find_pairs(ranking1, board1)
                ranking2 = find_pairs(ranking2, board2)
                while(True):
                    if ranking1[0] > ranking2[0]:
                        wins += 1
                        break
                    elif ranking1[0] < ranking2[0]:
                        losses += 1
                        break
                    elif len(ranking1) == 1:
                        ties += 1
                        break
                    else:
                        del ranking1[0]
                        del ranking2[0]
            equity = str(round((wins + 0.5 * ties) / matches * 100, precision))
            equities[(hands1[0], hands2[0])] = equity
            print("hand1:", hands1, " hand2:", hands2)
            print("matches:", matches, " wins:", wins, " ties:", ties, " losses:", losses, " equity:", equity)
            py.write("\t(\"" + hands1 + "\", \"" + hands2 + "\"): " + equity + ",\n")
            equity = str(round(100 - (wins + 0.5 * ties) / matches * 100, precision))
            equities[(hands2[0], hands1[0])] = equity
            py.write("\t(\"" + hands2 + "\", \"" + hands1 + "\"): " + equity + ",\n")
        else:
            print("hand1:", hands1, " hand2:", hands2)
            print("equity:", equities[(hands2, hands1)])
        '''print("hand1:", hands1, " hand2:", hands2)
        print("matches:", matches, " wins:", wins, " ties:", ties, " losses:", losses, " equity:", equity)
        txt.write(hands1 + " vs " + hands2 + " = " + equity + "\n")
        csv.write(equity)
        if hands2 == "AA":
            csv.write("\n")
        else:
            csv.write(",")
        py.write("\t(\"" + hands1 + "\", \"" + hands2 + "\"): " + equity)
        if hands1 == "AA" and hands2 == "AA":
            py.write("\n")
        else:
            py.write(",\n")'''

py.write("}")
#txt.close()
#csv.close()
py.close()
