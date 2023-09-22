import numpy

from random import randint


def fitness(x, mini=0):
    return sum(x) - mini


def roulette(pop, fit_scores):
    sum_fitness = sum(fit_scores)
    pick = numpy.random.uniform(0, sum_fitness)
    current = 0
    for j in range(len(pop)):
        current += fit_scores[j]
        if current > pick:
            return pop[j]


def crossover(parent1, parent2, prob):
    child1, child2 = parent1.copy(), parent2.copy()
    if prob > numpy.random.uniform():
        crossover_point = randint(1, len(parent1) - 2)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return [child1, child2]


def mutation(bitstring, prob):
    for j in range(len(bitstring)):
        if prob > numpy.random.uniform():
            bitstring[j] = 1 - bitstring[j]


if __name__ == '__main__':

    crossover_prob = 0.0
    mutation_prob = 0.001
    generations = []
    for times in range(0, 20):
        generation = 0
        population = [[randint(0, 1) for _ in range(100)] for _ in range(100)]
        best_eval = 0
        maximum = 0
        while maximum != 100:
            scores = [fitness(x) for x in population]
            minimum = min(scores)
            maximum = max(scores)
            scores = [fitness(x, minimum) for x in population]
            for chromosome in range(len(population)):
                if scores[chromosome] > best_eval:
                    best_eval = scores[chromosome]

            selected = [roulette(population, scores) for _ in range(len(population))]
            children = list()
            for i in range(0, len(population), 2):
                mom, dad = selected[i], selected[i + 1]
                for child in crossover(mom, dad, crossover_prob):
                    mutation(child, mutation_prob)
                    children.append(child)
            population = children
            generation += 1
        generations.append(generation)
    print("\nFinished with average", sum(generations) / len(generations), "!!")
