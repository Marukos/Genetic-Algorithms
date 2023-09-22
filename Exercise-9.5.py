import random

import numpy

from random import randint


def banana_fitness(x):
    return 100 * (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2


def powel_fitness(x):
    return (x[0] + 10 * x[1]) ** 2 + 5 * (x[2] - x[3]) ** 2 + (x[1] - 2 * x[2]) ** 4 + 10 * (x[0] - x[3]) ** 4


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
        if len(parent1) == 2:
            crossover_point = 1
        else:
            crossover_point = randint(1, len(parent1) - 2)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return [child1, child2]


def mutation(bitstring, prob, m, s):
    for j in range(len(bitstring)):
        if prob > numpy.random.uniform():
            bitstring[j] += random.gauss(m[j], s[j])


if __name__ == '__main__':
    crossover_prob = 0.8
    mutation_prob = 0.001
    function = 0
    average_scores = [0 for _ in range(101)]
    for _ in range(20):
        if not function:
            population = [[-12, 1] for _ in range(500)]
        else:
            population = [[3, -1, 0, 1] for _ in range(500)]

        for generation in range(1000):

            mean = numpy.mean(population, axis=0)
            std = numpy.std(population, axis=0)

            if not function:
                scores = [banana_fitness(x) for x in population]
            else:
                scores = [powel_fitness(x) for x in population]

            selected = [roulette(population, scores) for _ in range(len(population))]
            children = list()

            for i in range(0, len(population), 2):
                mom, dad = selected[i], selected[i + 1]
                for child in crossover(mom, dad, crossover_prob):
                    mutation(child, mutation_prob, mean, std)
                    children.append(child)
            population = children

            if generation % 10 == 9 or generation == 0:
                average_scores[generation // 10 + 1 - (generation == 0)] += min(scores)
    for i in range(101):
        print(average_scores[i]/20)
