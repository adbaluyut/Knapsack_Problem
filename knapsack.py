from datetime import datetime

import math
import random


class Item:
    
    def __init__(self, name="item", weight=0, value=0):
        self.name = name
        self.weight = weight
        self.value = value
    
    def __repr__(self):
        s = f"name: {self.name} | weight: {self.weight} | value: {self.value}"
        return s


class Bag:

    def __init__(self, name='', weight=0, fitness=0):
        self.name = name
        self.weight = weight
        self.fitness = fitness

    def __repr__(self):
        s = f"name: {self.name} | weight: {self.weight} | value: {self.fitness}"
        return s


# make the initial population
def create_population(pop_size, length):
    p = []
    for i in range(pop_size):
        gene = ''
        for j in range(length):
            gene += str(random.randint(0,1))
        p.append(Bag(name=gene))

    return p


# randomly create items
def create_items(list_size):
    items = []
    for i in range(list_size):
        w = random.randint(0, 60)
        val = random.randint(1, 10) # there is probably a better way to assign
        items.append(Item(chr(i + 65), w, val))

    return items


def print_list(items):
    print('+-----------------------------------------+')
    for it in items:
        print(it)    
    print('+-----------------------------------------+\n')


# calculate the weight and fitness of each Bag
def weight_and_fitness(pop, items, wght):
    for p in pop:
        w = 0
        v = 0
        for i, gene in enumerate(p.name):
            if gene == '1':
                w += items[i].weight
                v += items[i].value
        p.weight = w
        p.fitness = v if wght > w else v - 100

    return pop


# genetic algorithm logic
def ga(pop):
    n = 1000
    rand = random.random() * n
    if rand < (n * 0.95):
        print('crossover')
        return crossover(pop)

    print("Reproducing")

    return pop


# crossover logic
def crossover(pop):
    k = len(pop[0].name)
    new_pop = []
    for i in range(0, len(pop), 2):
        pop[i].name, pop[i + 1].name = uniform_crossover(pop[i], pop[i + 1])
    
        if random.random() * k < 1 / k:
            print("Mutating")
            pop[i].name = mutate(pop[i].name)
            pop[i + 1].name = mutate(pop[i + 1].name)

    return pop


# Uniform Crossover
def uniform_crossover(parent1, parent2):
    child1 = ''
    child2 = ''
    for i in range(len(parent1.name)):
        rand = random.randint(0, 1)
        if rand == 1:
            child1 += parent2.name[i]
            child2 += parent1.name[i]
        else:
            child1 += parent1.name[i]
            child2 += parent2.name[i]

    return child1, child2


def mutate(binary):
    if binary != '':
        word = ""
        li = []
        li[:] = binary
        rand = random.randint(0, len(binary) - 1)
        if binary[rand] == '0':
            li[rand] = '1'
        elif binary[rand] == '1':
            li[rand] = '0'
        word = word.join(li)
        
        return word

    return binary


def main():

    max_weight = 100
    population_size = 10
    item_list_size = 7

    item_list = create_items(item_list_size)
    # print_list(item_list)

    population = create_population(population_size, len(item_list))
    # print('population')
    # print(population)
    population = ga(population)
    # print(population)
    population = weight_and_fitness(population, item_list, max_weight)
    print_items(population)


if __name__ == "__main__":
    main()