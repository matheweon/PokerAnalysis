from collections import namedtuple
from equities2 import equities

csv = open("equities_vs_range.csv", "w")

range_frequencies = [
#   A  K  Q  J  T  9  8  7  6  5  4  3  2
    1, 1, 1, 1, 1, 0, 0, 0, 0,.5,.5,.5,.5, # A
    1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # K
    1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # Q
    0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, # J
    0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, # T
    0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, # 9
    0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, # 8
    0, 0, 0, 0, 0, 0, 0, 0,.5, 0, 0, 0, 0, # 7
    0, 0, 0, 0, 0, 0, 0, 0, 0,.5, 0, 0, 0, # 6
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,.5, 0, 0, # 5
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # 4
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # 3
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  # 2
]

range_frequencies = [1] * 169

range_frequencies = [
#   A  K  Q  J  T  9  8  7  6  5  4  3  2
    0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # A
    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # K
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # Q
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # J
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # T
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # 9
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # 8
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # 7
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # 6
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # 5
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # 4
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # 3
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  # 2
]

range_frequencies = [
#   A  K  Q  J  T  9  8  7  6  5  4  3  2
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, # A
    1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, # K
    1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, # Q
    1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, # J
    1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, # T
    1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, # 9
    1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, # 8
    0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, # 7
    0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, # 6
    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, # 5
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, # 4
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, # 3
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1  # 2
]

cards = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")

Hand = namedtuple("Hand", ["name", "rank1", "rank2", "frequency"])

hand_range = []
for i in range(169):
    if range_frequencies[i] != 0:
        hand_range.append(Hand(cards[i // 13] + cards[i % 13], 12 - i // 13, 12 - i % 13, range_frequencies[i]))

total_equities = {}
for rank1 in range(13):
    for rank2 in range(13):
        total_equity = 0
        total_combos = 0
        for hand in hand_range:
            rank3 = hand[1]
            rank4 = hand[2]
            combos = 0
            frequency = hand[3]
            if rank1 == rank2: # Pocket Pair
                if rank3 == rank4: # vs Pocket Pair
                    if rank1 == rank3: # vs Same Hand
                        combos = 6
                    else:
                        combos = 36
                elif rank3 > rank4: # vs Suited
                    if rank1 == rank3 or rank1 == rank4: # Shares Card
                        combos = 12
                    else:
                        combos = 24
                elif rank3 < rank4: # vs Unsuited
                    if rank1 == rank3 or rank1 == rank4: # Shares Card
                        combos = 36
                    else:
                        combos = 72
            elif rank1 > rank2: # Suited
                if rank3 == rank4: # vs Pocket Pair
                    if rank1 == rank3 or rank2 == rank3: # Shares Card
                        combos = 12
                    else:
                        combos = 24
                elif rank3 > rank4: # vs Suited
                    if rank1 == rank3 and rank2 == rank4: # Shares Both Cards
                        combos = 12
                    elif rank1 == rank3 or rank1 == rank4 or rank2 == rank3 or rank2 == rank4: # Shares Card
                        combos = 12
                    else:
                        combos = 16
                elif rank3 < rank4: # vs Unsuited
                    if rank1 == rank4 and rank2 == rank3: # Shares Both Cards
                        combos = 24
                    elif rank1 == rank3 or rank1 == rank4 or rank2 == rank3 or rank2 == rank4: # Shares Card
                        combos = 36
                    else:
                        combos = 48
            elif rank1 < rank2: # Unsuited
                if rank3 == rank4: # vs Pocket Pair
                    if rank1 == rank3 or rank2 == rank3: # Shares Card
                        combos = 36
                    else:
                        combos = 72
                elif rank3 > rank4: # vs Suited
                    if rank1 == rank4 and rank2 == rank3: # Shares Both Cards
                        combos = 24
                    elif rank1 == rank3 or rank1 == rank4 or rank2 == rank3 or rank2 == rank4: # Shares Card
                        combos = 36
                    else:
                        combos = 48
                elif rank3 < rank4: # vs Unsuited
                    if rank1 == rank3 and rank2 == rank4: # Shares Both Cards
                        combos = 84
                    elif rank1 == rank3 or rank1 == rank4 or rank2 == rank3 or rank2 == rank4: # Shares Card
                        combos = 108
                    else:
                        combos = 144
            total_combos += combos * frequency
            total_equity += equities[(cards[rank1] + cards[rank2], cards[rank3] + cards[rank4])] * combos * frequency
        total_equity = round(total_equity / total_combos, 2)
        total_equities[cards[rank1] + cards[rank2]] = total_equity

for rank1 in range(13):
    for rank2 in range(13):
        hand = cards[12 - rank1] + cards[12 - rank2]
        print(hand + ": " + str(total_equities[hand]) + " ", end='')
        csv.write(str(total_equities[hand]) + ",")
    print("")
    csv.write("\n")

csv.close()
