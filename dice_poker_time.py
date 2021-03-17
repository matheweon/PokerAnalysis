from functools import partial
from problems import dice_poker
from algorithms import genetic

import time

scoring = dice_poker.Scoring

best_scores = []
middle_scores = []
worst_scores = []

size = 10

for i in range(1000):
    dice_poker.fitnesses = {}
    dices = dice_poker.generate_dices(500)
    # target_value = sum([x for x in range(i+1)])
    fitness = partial(dice_poker.fitness, dices=dices, scoring=scoring)

    start = time.time()
    population, generations = genetic.run_evolution(
        populate_func=partial(genetic.generate_population, size=size, genome_length=16),
        fitness_func=fitness,
        fitness_limit=1000000,
        generation_limit=100
    )
    end = time.time()

    best_score = fitness(population[0])
    best_scores.append(best_score)
    best_trailing_average = 0
    count = 0
    for j in range(i-9, i+1):
        if j >= 0:
            best_trailing_average += best_scores[j]
            count += 1
    best_trailing_average = round(best_trailing_average / count)

    middle_score = fitness(population[size // 2])
    middle_scores.append(middle_score)
    middle_trailing_average = 0
    count = 0
    for j in range(i-9, i+1):
        if j >= 0:
            middle_trailing_average += middle_scores[j]
            count += 1
    middle_trailing_average = round(middle_trailing_average / count)

    worst_score = fitness(population[size - 1])
    worst_scores.append(worst_score)
    worst_trailing_average = 0
    count = 0
    for j in range(i-9, i+1):
        if j >= 0:
            worst_trailing_average += worst_scores[j]
            count += 1
    worst_trailing_average = round(worst_trailing_average / count)

    #print(dice_poker.fitnesses)

    print(f"Generation: {i}\t|\t{(end - start):e}s\t|\tBest: {best_score} Avg: {best_trailing_average}\t| \
        Middle: {middle_score} Avg: {middle_trailing_average}\t|\tWorst: {worst_score} Avg: {worst_trailing_average}\t| \
        {genetic.genome_to_string(population[0])}\t|\tSpecies: {len(dice_poker.fitnesses)}")
