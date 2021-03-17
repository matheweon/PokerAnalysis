from random import choices, randint, randrange, random
from typing import List, Optional, Callable, Tuple, Dict
from problems import poker
import random
import copy

Genome = Dict[str, Dict[str, int]]
Population = List[Genome]
PopulateFunc = Callable[[], Population]
FitnessFunc = Callable[[Genome], int]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]
PrinterFunc = Callable[[Population, int, FitnessFunc], None]


def generate_genome() -> Genome:
    genome = {"fitness": None, "sb-fold": {}, "sb-limp": {}, "sb-open": {}, "bb-fold": {}, "bb-call": {}}
    for action in ["sb-fold", "sb-limp", "sb-open", "bb-fold", "bb-call"]:
        #genome[action] = {}
        ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
        for pocket_pair in ranks:
            genome[action][pocket_pair + pocket_pair] = random.randint(0, 100)
        for card1 in range(13):
            for card2 in range(13):
                if card1 > card2:
                    genome[action][ranks[card1] + ranks[card2] + "o"] = random.randint(0, 100)
                    genome[action][ranks[card1] + ranks[card2] + "s"] = random.randint(0, 100)
    return genome


def generate_population(size: int) -> Population:
    return [generate_genome() for _ in range(size)]


def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    for i in range(500):
        rand_action = random.choice(list(a.keys()))
        rand_hand = random.choice(list(a[rand_action].keys()))
        # swap frequencies of a random action and random hand
        temp = a[rand_action][rand_hand]
        a[rand_action][rand_hand] = b[rand_action][rand_hand]
        b[rand_action][rand_hand] = temp
        '''print("-----------")
        print("a", a[rand_action][rand_hand])
        print("b", b[rand_action][rand_hand])'''
    return a, b



def mutation(genome: Genome, rate: float = 0.5) -> Genome:
    # WHAT HAVE I DONE BY ADDING "fitness" TO THE GENOME
    genome_without_fitness = {x: genome[x] for x in genome if x not in ["fitness"]}
    for action in genome_without_fitness:
        for hand in genome[action]:
            '''if hand == "22":
                print("-----------")
                print(genome[action][hand])'''

            genome[action][hand] += random.randint(-10, 10)
            if genome[action][hand] < 0:
                genome[action][hand] = 0
            elif genome[action][hand] > 100:
                genome[action][hand] = 100

            '''if hand == "22":
                print(genome[action][hand])'''
    return genome


def population_fitness(population: Population, fitness_func: FitnessFunc) -> int:
    return sum([fitness_func(genome) for genome in population])


def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    parents = choices(
        population=population,
        weights=[fitness_func(gene) for gene in population],
        k=2
    ) # FINALLY FIXED THIS BUG
    return copy.deepcopy(parents[0]), copy.deepcopy(parents[1])


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
        poker.fitnesses = {}
        population = sort_population(population, fitness_func)
        #print(len(poker.fitnesses))
        #print("test1", population[0]["sb-fold"] == population[1]["sb-fold"])

        if printer is not None:
            printer(population, i, fitness_func)

        '''if fitness_func(population[0]) >= fitness_limit:
            break'''

        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func)
            #offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a, offspring_b = parents[0], parents[1]
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

        #print("test2", population[0]["sb-fold"] == population[1]["sb-fold"])

        '''print("--------")
        for i in range(10):
            print(population[i]["sb-fold"]["22"], population[i]["sb-fold"]["33"], population[i]["sb-fold"]["44"], population[i]["sb-fold"]["55"])'''
        population = sort_population(population, fitness_func)
        '''print("sort")
        print("test3", population[0]["sb-fold"] == population[1]["sb-fold"])
        print("--------")
        for i in range(10):
            print(population[i]["sb-fold"]["22"], population[i]["sb-fold"]["33"], population[i]["sb-fold"]["44"], population[i]["sb-fold"]["55"])
        print("--------")'''

    print(poker.fitnesses)
    for i in range(10):
        #print(population[i]["sb-fold"]["22"], population[i]["sb-fold"]["33"], population[i]["sb-fold"]["44"], population[i]["sb-fold"]["55"])
        print(fitness_func(population[i]))
    population = sort_population(population, fitness_func)
    print("--------")
    for i in range(10):
        print(fitness_func(population[i]))

    return population, i
