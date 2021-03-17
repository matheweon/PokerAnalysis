from functools import partial
from problems import poker
from algorithms import genetic_poker

import time

best_scores = []
middle_scores = []
worst_scores = []

size = 10

for i in range(1000):
    fitness = partial(poker.fitness, num_hands=100)

    start = time.time()
    population, generations = genetic_poker.run_evolution(
        populate_func=partial(genetic_poker.generate_population, size=size),
        fitness_func=fitness,
        fitness_limit=1000000,
        generation_limit=10
    )
    end = time.time()

    '''print(poker.fitnesses)
    print(population[0])
    print(population[1])
    print(population[2])
    print(population[3])
    print(population[4])
    print(population[5])
    print(population[6])
    print(population[7])
    print(population[8])
    print(population[9])'''

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

    worst_score = fitness(population[-1])
    worst_scores.append(worst_score)
    worst_trailing_average = 0
    count = 0
    for j in range(i-9, i+1):
        if j >= 0:
            worst_trailing_average += worst_scores[j]
            count += 1
    worst_trailing_average = round(worst_trailing_average / count)

    print(f"Generation: {i}\t|\t{(end - start):e}s\t|\tBest: {best_score} Avg: {best_trailing_average}\t| \
        Middle: {middle_score} Avg: {middle_trailing_average}\t|\tWorst: {worst_score} Avg: {worst_trailing_average}\t| \
        {genetic_poker.genome_to_string(population[0])}\t|\tSpecies: {len(poker.fitnesses)}")
