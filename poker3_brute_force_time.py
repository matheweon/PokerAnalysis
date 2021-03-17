from functools import partial
from problems import poker3
from algorithms import genetic_poker3

import time
'''
PSEUDOCODE

1. generate sb_genome and bb_genome
2. calculate fitnesses
3. randomly flip a bit and until you find one that increases the fitness

ALSO

fix the equity generator so it same hand vs same hand is 50% and x vs y is the opposite of y vs x
'''
genome_length = 13 * 13
#sb_genome = genetic_poker2.generate_genome(genome_length)
#bb_genome = genetic_poker2.generate_genome(genome_length)
sb_genome = [0] * genome_length
bb_genome = [0] * genome_length
sb_genome = [
    1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]
bb_genome = [
    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]
sb_genome = [i * (poker3.bitsize - 1) for i in sb_genome]
bb_genome = [i * (poker3.bitsize - 1) for i in bb_genome]
iteration = 0
true_start = time.time()
while True:
    start = time.time()
    fitness = poker3.fitness(sb_genome, bb_genome)
    sb_genome, sb_optimal = genetic_poker3.mutation(sb_genome, bb_genome, "sb")
    bb_genome, bb_optimal = genetic_poker3.mutation(sb_genome, bb_genome, "bb")
    iteration += 1
    end = time.time()
    if iteration % 1 == 0:
        print("iteration:", iteration)
        print("time:", end - start)
        print("fitness:", poker3.fitness(sb_genome, bb_genome))
        print("sb_optimal:", sb_optimal)
        print("sb_genome:")
        for i in range(13):
            print(str(sb_genome[i*13:(i+1)*13]))
        print("bb_optimal:", bb_optimal)
        print("bb_genome:")
        for i in range(13):
            print(str(bb_genome[i*13:(i+1)*13]))
        if sb_optimal and bb_optimal:
            print("total_time:", time.time() - true_start)
            exit()
