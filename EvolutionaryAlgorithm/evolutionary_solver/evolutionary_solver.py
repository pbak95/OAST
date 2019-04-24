import copy
import math
from math import ceil

from model import Network, Demand
from solution_checker import check_solution
from random import randint, random


def mock_solution(network) -> Network:
    links = network.links_list
    for link in links:
        link.number_of_fibers = 1
        link.number_of_signals = 2

    for demand in network.demands_list:
        demand.solution_number_of_demand_paths = demand.number_of_demand_paths
        for path in demand.demand_path_list:
            path.solution_path_signal_count = 1

    return network


def evolutionary_solve(network: Network) -> Network:
    population_size = 5
    mutation_probability = 0.1
    # Solve here
    # TODO add evolutionary algorithm
    check_solution(network)

    # initialisation of population
    population = init_population(population_size, network)
    for idx, chromosome in enumerate(population):
        print('Chromosome: ', idx)
        chromosome.print()

    # loop START

    # pairs selection
    pairs = select_pairs(population)
    for idx, pair in enumerate(pairs):
        print('Pair: ', idx)
        pair[0].print()
        pair[1].print()
    # crossover inside pairs, new population consists of children from each pair in pairs
    new_population = make_crossover(pairs)

    # mutation in new population
    for chromosome in new_population:
        chromosome.mutate(mutation_probability)

    # update population based on fitnesses

    # stopping criterium

    # loop END

    return mock_solution(network)


def init_population(population_number: int, network: Network) -> list:
    chromosomes = []
    for _ in range(0, population_number):
        chromosomes.append(Chromosome(network))
    return chromosomes


def select_pairs(population: list) -> list:
    population_by_fitness = sorted(population)
    return list(zip(population_by_fitness[::2], population_by_fitness[1::2]))


def make_crossover(pairs: list) -> list:
    new_population = []
    for pair in pairs:
        new_pair = crossover(pair)
        new_population.append(new_pair[0])
        new_population.append(new_pair[1])
    return new_population


def crossover(parents_pair):
    first_child_genes = []
    second_child_genes = []
    for idx in range(0, len(parents_pair[0].genes)):
        if random() < 0.5:
            first_child_genes.append(parents_pair[0].genes[idx])
            second_child_genes.append(parents_pair[1].genes[idx])
        else:
            first_child_genes.append(parents_pair[1].genes[idx])
            second_child_genes.append(parents_pair[0].genes[idx])

    # copy Network metadata which is common for all Chromosomes
    first_child: Chromosome = copy.deepcopy(parents_pair[0])
    first_child.genes = first_child_genes
    first_child.update_fitness()

    second_child: Chromosome = copy.deepcopy(parents_pair[0])
    second_child.genes = second_child_genes
    second_child.update_fitness()

    return first_child, second_child


class Chromosome(object):
    def __init__(self, network: Network):
        """
        Represents full solution - load for all demands
        :param network:
        """
        self.number_of_links = network.number_of_links
        self.links_list = network.links_list
        self.number_of_demands = network.number_of_demands
        self.demands_list = network.demands_list
        self.genes = self.init_genes(self.demands_list, network.longest_demand_path)
        self.fitness = self.calculate_fitness()

    def __lt__(self, other):
        return self.fitness < other.fitness

    @staticmethod
    def init_genes(demands_list: list, paths_number: int) -> list:
        genes = []
        for idx in range(0, len(demands_list)):
            genes.append(Gene(demands_list[idx], paths_number))
        return genes

    def mutate(self, mutation_probability):
        for gene in self.genes:
            if random() < mutation_probability:
                gene.mutate()

    def update_fitness(self):
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self) -> int:
        """
        Calculate chromosome fitness which is the summary cost of all modules for each link in the network. Modules
        number for each link is calculated based on link load.
        !!! Lower fitness is better. !!!
        If the modules number for particular link exceeds possible modules number, fitness is set to infinity, which
        means that it is impossible to create such link
        """
        fitness = 0
        link_load = self.calculate_link_load()
        for link in self.links_list:
            modules_number = ceil(link_load[link.link_id - 1] / link.single_module_capacity);
            if modules_number > link.maximum_number_of_modules:
                fitness = math.inf
                break
            else:
                fitness += modules_number * link.module_cost
        return fitness

    def calculate_link_load(self) -> list:
        """
        Calculate link load on the basis of demand volume for each demand path
        :return: list of link load for each link where load index is equal (link_id - 1)
        """
        load = [0] * self.number_of_links
        for demand in range(0, self.number_of_demands):
            for path in range(0, self.demands_list[demand].number_of_demand_paths):
                flows_running_this_path = self.genes[demand].paths[path]
                for linkInPath in self.demands_list[demand].demand_path_list[path].link_list:
                    load[linkInPath - 1] = load[linkInPath - 1] + flows_running_this_path
        return load

    def print(self):
        for gene in self.genes:
            gene.print()
        self.print_link_load()
        print('Fitness: ', self.fitness)
        print('\n')

    def print_link_load(self):
        print('Link load: ', self.calculate_link_load())


class Gene(object):
    def __init__(self, demand: Demand,  paths_number: int):
        """
        Represents volume load among all paths for particular demand
        :param demand: demand which we want to split into paths
        :param paths_number: maximum number of paths for all demands to have same array size for all paths in Gene
        """
        self.paths = [0 for x in range(paths_number)]
        self.demand = demand
        self.init_paths_values()

    def init_paths_values(self):
        for demand_path_id in range(0, self.demand.number_of_demand_paths):
            if demand_path_id == 0:
                self.paths[demand_path_id] = randint(0, self.demand.demand_volume)
            elif demand_path_id == self.demand.number_of_demand_paths - 1:
                if self.demand.number_of_demand_paths > 1:
                    self.paths[demand_path_id] = self.demand.demand_volume - sum(self.paths[0:demand_path_id])
                else:
                    self.paths[demand_path_id] = self.demand.demand_volume
            else:
                self.paths[demand_path_id] = randint(0, self.demand.demand_volume - sum(self.paths[0:demand_path_id]))

    def mutate(self):
        if self.demand.number_of_demand_paths == 2:
            self.paths[0], self.paths[1] = self.paths[1], self.paths[0]
        elif self.demand.number_of_demand_paths > 2:
            indexes = list(range(0, self.demand.number_of_demand_paths))
            first_idx = indexes.pop(randint(0, self.demand.number_of_demand_paths - 1))
            second_idx = indexes.pop(randint(0, len(indexes) - 1))
            self.paths[first_idx], self.paths[second_idx] = self.paths[second_idx], self.paths[first_idx]

    def print(self):
        print(self.paths)
