from functools import partial
from problems import poker2
from algorithms import genetic_poker2

import time

'''weight_limit = 3000

for i in range(2, 80):
    things = poker2.generate_things(i)
    target_value = sum([x for x in range(i+1)])
    fitness = partial(poker2.fitness, things=things, weight_limit=weight_limit)

    start = time.time()
    population, generations = genetic_poker2.run_evolution(
        populate_func=partial(genetic_poker2.generate_population, size=10, genome_length=len(things)),
        fitness_func=fitness,
        fitness_limit=sum([x for x in range(i+1)]),
        generation_limit=100
    )
    end = time.time()

    print(f"{i}\t|\t{generations}\t|\t{(end - start):e}s\t|\t{(fitness(population[0])/target_value*100):.2f}%\t|\t{genetic_poker2.genome_to_string(population[0])}")'''


num_matchups = 100
size = 50
genome_length = 13 * 13 * 2
fitness_limit = 1000000
#op_genome = genetic_poker2.generate_genome(genome_length)
op_genome = [1] * genome_length
generation_num = 0
generation_limit = 5
matchups = poker2.generate_matchups(num_matchups)

while True:
    generation_num += 1
    fitness = partial(poker2.fitness, matchups=matchups, op_genome=op_genome)
    start = time.time()
    population, generations = genetic_poker2.run_evolution(
        populate_func=partial(genetic_poker2.generate_population, size=size, genome_length=genome_length),
        fitness_func=fitness,
        fitness_limit=fitness_limit,
        generation_limit=generation_limit
    )
    end = time.time()

    print(f"{generation_num}\t|\t{generations}\t|\t{(end - start):e}s\t|\t{(fitness(population[0])):.2f}\t|\t{(fitness(population[len(population) // 2])):.2f}\t|\t{(fitness(population[-1])):.2f}\t|\t{genetic_poker2.genome_to_string(population[0])}")
