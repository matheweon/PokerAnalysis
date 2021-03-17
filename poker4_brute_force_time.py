from functools import partial
from problems import poker4
from algorithms import genetic_poker4

import time

genome_length = 13 * 13
#sb_genome = genetic_poker2.generate_genome(genome_length)
#bb_genome = genetic_poker2.generate_genome(genome_length)
sb_genome = [1] * genome_length
bb_genome = [1] * genome_length
iteration = 0
true_start = time.time()
while True:
    start = time.time()
    fitness = poker4.fitness(sb_genome, bb_genome)
    sb_genome, sb_optimal = genetic_poker4.mutation(sb_genome, bb_genome, "sb")
    bb_genome, bb_optimal = genetic_poker4.mutation(sb_genome, bb_genome, "bb")
    iteration += 1
    end = time.time()
    if iteration % 1 == 0:
        print("iteration:", iteration)
        print("time:", end - start)
        print("fitness:", poker4.fitness(sb_genome, bb_genome))
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
