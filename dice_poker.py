from algorithms.genetic import Genome
from collections import namedtuple
import random

Dice = namedtuple('Dice', ['die1', 'die2', 'die3', 'die4', 'die5'])

example = [
    Dice(1, 2, 3, 4, 5),
    Dice(6, 1, 5, 2, 2),
    Dice(6, 6, 6, 6, 6)
]

Scoring = {
    "No Pair": -5,
    "One Pair": -3,
    "Two Pair": -1,
    "Three of a Kind": 0,
    "Straight": 1,
    "Full House": 1,
    "Four of a Kind": 3,
    "Five of a Kind": 5
}

def generate_dices(num: int) -> [Dice]:
    return [Dice(random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)) for i in range(1, num+1)]

fitnesses = {}

def fitness(genome: Genome, dices: [Dice], scoring: {}) -> int:
    if tuple(genome) in fitnesses:
        return fitnesses[tuple(genome)]

    # Decode genome
    total_score = 0
    for i in range(len(dices)):
        score = 0
        for j in range(10):
            score += random.randint(1, 6) + random.randint(1, 6)
            if len(genome) > score and genome[score] == 0:
                break
            if score > 16:
                score -= 16
        total_score += score

    fitnesses[tuple(genome)] = total_score
    return total_score
    '''
    # Decode genome
    if_match_weight, if_unmatch_weight = 0, 0
    for i in range(8):
        if_match_weight += 2**i * genome[i] - 2**3
    for i in range(8):
        if_unmatch_weight += 2**i * genome[i+8] - 2**3

    # Decide whether to roll each die
    dice_rolls = []
    for round in range(len(dices)):
        dice_rolls.append([])
        for die in range(4):
            weight = 0
            for other_die in range(4):
                if (die != other_die):
                    if (dices[round][die] == dices[round][other_die]):
                        weight += if_match_weight
                    else:
                        weight += if_unmatch_weight
            #print(weight)
            if (weight > random.randint(0, 2**7)):
                dice_rolls[round].append(die)

    #print(len(dice_rolls[0]))
    # Roll the dice
    for round in range(len(dices)):
        dices_temp = [dices[round][0], dices[round][1], dices[round][2], dices[round][3], dices[round][4]]
        for die in dice_rolls[round]:
            dices_temp[die] = random.randint(1, 6)
        dices[round] = Dice(dices_temp[0], dices_temp[1], dices_temp[2], dices_temp[3], dices_temp[4])

    # Scoring
    score = 0
    for round in range(len(dices)):
        if (1, 2, 3, 4, 5) in dices[round] or (2, 3, 4, 5, 6) in dices[round]:
            score += scoring["Straight"]
            continue
        sets = [0, 0, 0, 0, 0, 0]
        for die in dices[round]:
            sets[die-1] += 1
        if 5 in sets:
            score += scoring["Five of a Kind"]
        elif 4 in sets:
            score += scoring["Four of a Kind"]
        elif 3 in sets and 2 in sets:
            score += scoring["Full House"]
        elif 3 in sets:
            score += scoring["Three of a Kind"]
        elif 2 not in sets:
            score += scoring["No Pair"]
        else:
            count = 0
            for i in range(6):
                if sets[i] == 2:
                    count += 1
            if count == 2:
                score += scoring["Two Pair"]
            else:
                score += scoring["One Pair"]

    fitnesses[tuple(genome)] = score
    return score'''

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
