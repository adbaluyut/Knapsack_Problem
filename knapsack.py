from datetime import datetime

import math
import random


class Item:

    def __init__(self, name="item", weight=0, value=0):
        self.name = name
        self.weight = weight
        self.value = value
    #
    # def __repr__(self):
    #     s = f"name: {self.name} | weight: {self.weight} | value: {self.value}"
    #     return s


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


def print_items(items):
    print('+-----------------------------------------+')
    for it in items:
        print(it)
    print('+-----------------------------------------+\n')


# calculate the weight and fitness of each Bag
def weight_and_fitness(pop, items, wght):
    #print_items(pop)
    print(pop[0].name)
    # print("here")
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
def ga(pop, pop_size):
    #select which parents are going to reproduce
    n = 1000
    rand = random.random() * n
    # if rand < (n * 0.95):
    crossover(pop, pop_size)
    return pop


# crossover logic //
def crossover(pop, pop_size):
    k = len(pop[0].name)
    new_pop = []

    first = random.randint(0,pop_size-1)
    second = random.randint(0, pop_size-1)
    while second == first:
        # print("Oopsie")
        second = random.randint(0, pop_size)
    # print("first", first, " second", second )
    new1, new2 = uniform_crossover(pop[first], pop[second])

    if random.random() * k < 1 / k:
        # print("Mutating")
        new1.name = mutate(new1.name)
        new2.name = mutate(new2.name)

    pop = cull_the_weak(pop, pop_size, new1, new2)

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
    new1 = Bag(child1, 0, 0)
    new2 = Bag(child2,0,0)
    return new1, new2


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


def cull_the_weak(pop, pop_size, new1, new2):
    l1 = 10000000000 # very large number
    l2 = 10000000000
    l1index = 800 #random indexes
    l2index = 800
    for p in range(0, pop_size):
        if pop[p].fitness < l1:
            l1 = pop[p].fitness
            l1index = p
    for p in range(0, pop_size):
        if pop[p].fitness < l2 and p != l1index:
            l2 = pop[p].fitness
            l2index = p
    # print("old l1", pop[l1index].name, " ", pop[l1index].fitness, " : ",  "old l2", pop[l2index].name, " ", pop[l2index].fitness)
    pop[l1index] = new1
    pop[l2index] = new2
    # print("new l1", pop[l1index].name, " ", pop[l1index].fitness, " : ",  "new l2", pop[l2index].name, " ", pop[l2index].fitness)
    return pop

def best(pop, pop_size):
    bestIndex =10000000000
    best = 0
    for p in range(0, pop_size):
        if pop[p].fitness > best:
            best = pop[p].fitness
            bestIndex = p
    print("the best solution found had a weight of ", pop[bestIndex].weight, " and a total value of ", best)
    print(pop[bestIndex])
def main():

    max_weight = 100
    population_size = 100
    item_list_size = 7

    item_list = create_items(item_list_size)
    print_items(item_list)

    population = create_population(population_size, len(item_list))

    population = weight_and_fitness(population, item_list, max_weight)

    # print(population)
    for x in range(0,1000):
        population = ga(population, population_size)
        population = weight_and_fitness(population, item_list, max_weight)
        # print_items(population)
    best(population, population_size)

if __name__ == "__main__":
    main()
