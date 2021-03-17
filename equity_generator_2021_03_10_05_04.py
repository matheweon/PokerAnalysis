from collections import namedtuple
import copy

Card = namedtuple("Card", ["name", "rank", "suit"])
Hand = namedtuple("Hand", ["name", "card1", "card2", "type"])

output = open("equities.txt", "w")

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
        kicker = sorted(pair_count[1], reverse=True)[0]
        return [7, pair_count[4][0], kicker] # Four Of A Kind
    elif len(pair_count[3]) == 1 and len(pair_count[2]) >= 1:
        pair = sorted(pair_count[2], reverse=True)[0]
        return [6, pair_count[3][0], pair] # Full House
    elif ranking[0] > 3:
        return ranking # Return if better than trips
    elif len(pair_count[3]) == 2:
        trips = sorted(pair_count[3], reverse=True)[0]
        kickers = sorted((pair_count[1] + trips[1]), reverse=True)
        return [3, trips, kickers[0], kickers[1]] # Three Of A Kind (with two trips)
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
        matchups = []
        matches = 0
        wins = 0
        ties = 0
        losses = 0
        for hand1 in hands[hands1]:
            for hand2 in hands[hands2]:
                if not (hand1[1] == hand2[1] or hand1[1] == hand2[2] or hand1[2] == hand2[1] or hand1[2] == hand2[2]):
                    matchups.append((hand1, hand2))
        for matchup in matchups:
            use_deck = copy.deepcopy(full_deck)
            use_deck.remove(matchup[0][1])
            use_deck.remove(matchup[0][2])
            use_deck.remove(matchup[1][1])
            use_deck.remove(matchup[1][2])
            for card1 in use_deck:
                for card2 in use_deck:
                    if card2 == card1:
                        break
                    for card3 in use_deck:
                        if card3 == card1 or card3 == card2:
                            break
                        for card4 in use_deck:
                            if card4 == card1 or card4 == card2 or card4 == card3:
                                break
                            for card5 in use_deck:
                                if card5 == card1 or card5 == card2 or card5 == card3 or card5 == card4:
                                    break
                                matches += 1
                                board = [card1, card2, card3, card4, card5]
                                board1 = board + [hand1[1], hand1[2]]
                                board2 = board + [hand2[1], hand2[2]]
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
                                            #print("tie")
                                            break
                                        elif ranking1[1] > ranking2[1]:
                                            wins += 1
                                            print("win")
                                            break
                                        else:
                                            losses += 1
                                            print("lose")
                                            break
                                    else:
                                        wins += 1
                                        print("win")
                                        break
                                elif ranking2[0] == 8:
                                    losses += 1
                                    print("lose")
                                    break

                                ranking1 = find_straight(ranking1, board1)
                                ranking2 = find_straight(ranking2, board2)
                                ranking1 = find_pairs(ranking1, board1)
                                ranking2 = find_pairs(ranking2, board2)
                                print(matches)
                                print("ranking1", ranking1)
                                print("ranking2", ranking2)
                                while(True):
                                    if ranking1[0] > ranking2[0]:
                                        wins += 1
                                        print("win")
                                        break
                                    elif ranking1[0] < ranking2[0]:
                                        losses += 1
                                        print("lose")
                                        break
                                    elif len(ranking1) == 1:
                                        ties += 1
                                        #print("tie")
                                        break
                                    else:
                                        del ranking1[0]
                                        del ranking2[0]

        print("hand1:", hand1)
        print("hand2:", hand2)
        print("wins:", wins, " ties:", ties, " losses: ", losses)






for hand in hands:
    output.writelines(hands[hand])

#output.writelines(hands)
output.close()
