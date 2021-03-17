from random import choices, randint, randrange, random
from typing import List, Optional, Callable, Tuple
from problems import poker4
import copy
import math

Genome = List[int]
Population = List[Genome]
PopulateFunc = Callable[[], Population]
FitnessFunc = Callable[[Genome], int]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]
PrinterFunc = Callable[[Population, int, FitnessFunc], None]


def generate_genome(length: int) -> Genome:
    return choices([0, 1], k=length)


def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]


def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("Genomes a and b must be of same length")

    length = len(a)
    if length < 2:
        return a, b

    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]

mutation_rate = 0.2
def mutation(sb_genome: Genome, bb_genome: Genome, mutate_which: str) -> Genome:
    fitness = poker4.fitness(sb_genome, bb_genome)
    fitnesses = {}
    if mutate_which == "sb":
        for i in range(len(sb_genome)):
            genome = copy.deepcopy(sb_genome)
            for b in range(poker4.bitsize):
                genome[i] = (genome[i] + 1) % poker4.bitsize
                new_fitness = poker4.fitness(genome, bb_genome)
                if new_fitness > fitness:
                    fitnesses[(i, genome[i])] = round(new_fitness - fitness, 4)
        if len(fitnesses) == 0:
            print("sb_possible_mutations: OPTIMAL")
            return sb_genome, True
        else:
            '''
            print("sb_possible_mutations:", len(fitnesses))
            for item in sorted(fitnesses.items(), key=lambda item: item[1], reverse=True):
                print(poker3.inv_card_dict[item[0][0] // 13] + poker3.inv_card_dict[item[0][0] % 13] + ", " + str(item[0][1]) + ", " + str(item[1]))
            mutation = choices(list(fitnesses.keys()), weights=list(fitnesses.values()), k=1)[0]
            print("mutation:", poker3.inv_card_dict[mutation[0] // 13] + poker3.inv_card_dict[mutation[0] % 13], "-->", mutation[1])
            sb_genome[mutation[0]] = mutation[1]
            return sb_genome, False
            '''

            print("sb_possible_mutations:", len(fitnesses))
            #possible_mutations = sorted(fitnesses.items(), key=lambda item: item[1])
            # change this to numpy sample eventually
            possible_mutations = choices(list(fitnesses.items()), weights=[i**3 for i in list(fitnesses.values())], k=math.ceil(len(fitnesses)*mutation_rate))
            for mutation in possible_mutations:
                sb_genome[mutation[0][0]] = mutation[0][1]
                print(poker4.inv_card_dict[mutation[0][0] // 13] + poker4.inv_card_dict[mutation[0][0] % 13] + ", " + str(mutation[0][1]) + ", " + str(mutation[1]))
            return sb_genome, False
    else:
        for i in range(len(bb_genome)):
            genome = copy.deepcopy(bb_genome)
            for b in range(poker4.bitsize):
                genome[i] = (genome[i] + 1) % poker4.bitsize
                new_fitness = poker4.fitness(sb_genome, genome)
                if new_fitness < fitness:
                    fitnesses[(i, genome[i])] = round(fitness - new_fitness, 4)
        if len(fitnesses) == 0:
            print("bb_possible_mutations: OPTIMAL")
            return bb_genome, True
        else:
            print("bb_possible_mutations:", len(fitnesses))
            #possible_mutations = sorted(fitnesses.items(), key=lambda item: item[1])
            possible_mutations = choices(list(fitnesses.items()), weights=[i**3 for i in list(fitnesses.values())], k=math.ceil(len(fitnesses)*mutation_rate))
            for mutation in possible_mutations:
                bb_genome[mutation[0][0]] = mutation[0][1]
                print(poker4.inv_card_dict[mutation[0][0] // 13] + poker4.inv_card_dict[mutation[0][0] % 13] + ", " + str(mutation[0][1]) + ", " + str(mutation[1]))
            return bb_genome, False


def population_fitness(population: Population, fitness_func: FitnessFunc) -> int:
    return sum([fitness_func(genome) for genome in population])


def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    weights = [fitness_func(gene) for gene in population]
    offset = min(weights)
    positiveweights = [z - offset + 1 for z in weights]
    return choices(
        population=population,
        weights=positiveweights,
        k=2
    )


def sort_population(population: Population, fitness_func: FitnessFunc) -> Population:
    return sorted(population, key=fitness_func, reverse=True)


def genome_to_string(genome: Genome) -> str:
    return "".join(map(str, genome))


def print_stats(population: Population, generation_id: int, fitness_func: FitnessFunc):
    print("GENERATION %02d" % generation_id)
    print("=============")
    print("Population: [%s]" % ", ".join([genome_to_string(gene) for gene in population]))
    print("Avg. Fitness: %f" % (population_fitness(population, fitness_func) / len(population)))
    sorted_population = sort_population(population, fitness_func)
    print(
        "Best: %s (%f)" % (genome_to_string(sorted_population[0]), fitness_func(sorted_population[0])))
    print("Worst: %s (%f)" % (genome_to_string(sorted_population[-1]),
                              fitness_func(sorted_population[-1])))
    print("")

    return sorted_population[0]


def run_evolution(
        populate_func: PopulateFunc,
        fitness_func: FitnessFunc,
        fitness_limit: int,
        selection_func: SelectionFunc = selection_pair,
        crossover_func: CrossoverFunc = single_point_crossover,
        mutation_func: MutationFunc = mutation,
        generation_limit: int = 100,
        printer: Optional[PrinterFunc] = None) \
        -> Tuple[Population, int]:
    population = populate_func()

    for i in range(generation_limit):
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)

        if printer is not None:
            printer(population, i, fitness_func)

        if fitness_func(population[0]) >= fitness_limit:
            break

        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)

    return population, i
