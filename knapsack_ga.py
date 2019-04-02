from classes import Knapsack, Item
import matplotlib.pyplot as plt
import random
import operator
import copy


# Initialization of the 'population' of Knapsacks with 'items'

def init_pop(pop_size, items):
    return [Knapsack(items) for i in range(pop_size)]


# Evaluation of population

def eval_pop(pop, threshold):
    for p in pop:
        p.evaluate(threshold)


# Generating a single child from two parents based on Order Crossover (OX)

def breed(parent1, parent2):
    child_packed = copy.copy(parent2.packed)

    start = int(random.random() * len(parent1.packed))
    end = int(random.random() * len(parent1.packed))

    gene_beg = min(start, end)
    gene_end = max(start, end)

    for i in range(gene_beg, gene_end):
        child_packed[i] = parent1.packed[i]

    child = copy.copy(parent1)
    child.packed = child_packed

    return child


# Crossover of the population - generating the offspring.

def crossover(population, elite_size):

    mating_pool = []
    offspring = []

    # Elite selection - some part of best fit individuals goes to offspring directly.

    sorted_pop = sorted(population, key=operator.attrgetter('fitness'), reverse=True)
    for i in range(elite_size):
        mating_pool.append(copy.copy(sorted_pop[i]))
        offspring.append(copy.copy(sorted_pop[i]))

    # Wheel of fortune - more fit individuals have higher chance of getting into mating pool.

    dist_normal = 0
    for p in population:
        dist_normal += p.fitness

    for i in range(len(population) - elite_size):
        r = random.uniform(0, 1)
        p = 0
        while r > 0:
            r -= population[p].fitness / dist_normal
            p += 1
        mating_pool.append(population[p - 1])

    # Shuffling the mating pool.

    random.shuffle(mating_pool)

    # Breeding the remaining individuals of new population.

    for i in range(len(population) - elite_size):
        kid = breed(mating_pool[i], mating_pool[len(mating_pool) - i - 1])
        offspring.append(kid)

    return offspring


# Mutating

def mutate(population, elite):
    for i in range(elite, len(population)):
        r1 = random.uniform(0, 1)
        if r1 < mutation_probability:
            r2 = random.randint(0, len(population[i].packed)-1)
            population[i].packed[r2] = not population[i].packed[r2]


pop_size = 25
mutation_probability = 0.75
elite = int(pop_size * 0.2)
max_iter = 100
threshold = 165

items = [Item(92, 23), Item(57, 31), Item(49, 29), Item(68, 44), Item(60, 53),
         Item(43, 38), Item(67, 63), Item(84, 85), Item(87, 89), Item(72, 82)]

pop = init_pop(pop_size, items)
eval_pop(pop, threshold)
progress = [pop[0].fitness]

for i in range(max_iter):
    pop = crossover(pop, elite)
    mutate(pop, elite)
    eval_pop(pop, threshold)
    progress.append(pop[0].fitness)

print("Solution: " + str(pop[0]))
print("Value of the best solution: " + str(pop[0].fitness))

plt.plot(progress)
plt.show()
