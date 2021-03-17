from functools import partial
from problems import poker2
from algorithms import genetic_poker2

import time
'''
PSEUDOCODE

1. generate sb_genome and bb_genome
2. calculate fitnesses
3. randomly flip a bit and until you find one that increases the fitness

ALSO

fix the equity generator so it same hand vs same hand is 50% and x vs y is the opposite of y vs x
'''
genome_length = 13 * 13 * 2
matchups = poker2.generate_matchups(0)
sb_genome = genetic_poker2.generate_genome(genome_length)
bb_genome = genetic_poker2.generate_genome(genome_length)
sb_genome = [1] * genome_length
bb_genome = [1] * genome_length
iteration = 0
flipped_bits = 1
mutation_attempt_limit = 1000
true_start = time.time()
while True:
    start = time.time()
    my_fitness = poker2.fitness(sb_genome, matchups, bb_genome)
    counter = 0
    my_limit = False
    while True:
        if counter >= mutation_attempt_limit:
            my_limit = True
            break
        counter += 1
        new_genome = genetic_poker2.mutation(sb_genome, flipped_bits, 1)
        new_fitness = poker2.fitness(new_genome, matchups, bb_genome)
        if new_fitness > my_fitness:
            sb_genome = new_genome
            break
    op_fitness = poker2.fitness(bb_genome, matchups, sb_genome)
    counter = 0
    op_limit = False
    while True:
        if counter >= mutation_attempt_limit:
            op_limit = True
            break
        counter += 1
        new_genome = genetic_poker2.mutation(bb_genome, flipped_bits, 1)
        new_fitness = poker2.fitness(new_genome, matchups, sb_genome)
        if new_fitness > op_fitness:
            bb_genome = new_genome
            break
    iteration += 1
    end = time.time()
    if iteration % 1 == 0:
        print("iteration:", iteration)
        print("time:", end - start)
        print("my_fitness:", poker2.fitness(sb_genome, matchups, bb_genome))
        print("my_limit:", my_limit)
        print("sb_genome:")
        for i in range(13):
            print(str(sb_genome[i*13:(i+1)*13]) + " - " + str(sb_genome[(i+13)*13:(i+14)*13]))
        print("op_fitness:", poker2.fitness(bb_genome, matchups, sb_genome))
        print("op_limit:", op_limit)
        print("bb_genome:")
        for i in range(13):
            print(str(bb_genome[i*13:(i+1)*13]) + " - " + str(bb_genome[(i+13)*13:(i+14)*13]))
        if my_limit and op_limit and sb_genome == bb_genome:
            print("total_time:", time.time() - true_start)
            exit()
