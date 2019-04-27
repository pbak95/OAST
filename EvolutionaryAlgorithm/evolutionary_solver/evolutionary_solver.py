import copy
import math
import time

from math import ceil

from evolutionary_solver.config_reader import get_config
from model import Network, Demand
from random import randint, random, seed


def evolutionary_solve(network: Network) -> Network:
    config = get_config()
    seed(config.seed)
    population_size = config.population_size
    mutation_probability = config.mutation_probability

    # initialisation of population
    population = init_population(population_size, network)

    best_chromosome = None
    i = 0

    if config.stop == 'mut':
        mutation_counter = 0
    if config.stop == 'time':
        start = time.time()
    while True:

        print("OLD POPULATION:")
        for o in population:
            o.update_fitness()
            o.print()

        # pairs selection
        pairs = select_pairs(population)
        new_population = make_crossover(pairs)

        # mutation in new population
        for chromosome in new_population:
            if chromosome.mutate(mutation_probability) and config.stop == 'mut':
                mutation_counter += 1

        # set next population parents based on current population and their childes
        population = sorted(sorted(population)[0:2] + sorted(new_population + population)[0:population_size - 2])

        print("NEW POPULATION:")
        for n in population:
            n.print()

        # stopping criterium
        if config.stop == 'best_iter':
            if i > 0 and i % config.stop_arg == 0:
                if best_chromosome.fitness == population[0].fitness:
                    print_best_solution(best_chromosome, i, 'BEST ITERATION')
                    break

            if i % config.stop_arg == 0:
                best_chromosome = population[0]
        elif config.stop == 'iter':
            best_chromosome = population[0]
            if i == config.stop_arg:
                print_best_solution(best_chromosome, i, 'NUMBER OF ITERATIONS')
                break
        elif config.stop == 'mut':
            best_chromosome = population[0]
            if mutation_counter >= config.stop_arg:
                print_best_solution(best_chromosome, i, 'MINIMUM NUMBER OF MUTATIONS {}, PERFORMED {}'.format(
                    config.stop_arg, mutation_counter))
                break
        elif config.stop == 'time':
            best_chromosome = population[0]
            end = time.time()
            time_interval = end - start
            if time_interval >= config.stop_arg:
                print_best_solution(best_chromosome, i, 'MINIMUM ELAPSED TIME {} s, TAKES {} s'.format(
                    config.stop_arg, time_interval))
                break
        i += 1

    result_network = update_network_link_parameters(best_chromosome, network)
    for link in result_network.links_list:
        link.print_result()
    return result_network


def print_best_solution(chromosome, iter, stop):
    print('STOPPING CRITERIUM ACHIEVED: ', stop)
    print('BEST SOLUTION IN ITERATION: ', iter)
    chromosome.print()

def init_population(population_number: int, network: Network) -> list:
    chromosomes = []
    for _ in range(0, population_number):
        chromosomes.append(Chromosome(network))
    return sorted(chromosomes)


def select_pairs(population: list) -> list:
    return list(zip(population[::2], population[1::2]))


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
            first_child_genes.append(copy.deepcopy(parents_pair[0].genes[idx]))
            second_child_genes.append(copy.deepcopy(parents_pair[1].genes[idx]))
        else:
            first_child_genes.append(copy.deepcopy(parents_pair[1].genes[idx]))
            second_child_genes.append(copy.deepcopy(parents_pair[0].genes[idx]))

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

    def mutate(self, mutation_probability) -> bool:
        mutation = False
        for gene in self.genes:
            if random() < mutation_probability:
                mutation = True
                gene.mutate()
                self.update_fitness()
        return mutation

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
        # for gene in self.genes:
        #     gene.print()
        self.print_link_load()
        print('Fitness: ', self.fitness)
        # self.update_fitness()
        # print('UPDATED Fitness: ', self.fitness)
        print('\n')

    def print_link_load(self):
        print('Link load: ', self.calculate_link_load())


class Gene(object):
    def __init__(self, demand: Demand, paths_number: int):
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


def update_network_link_parameters(best_chromosome: Chromosome, network: Network) -> Network:
    link_load = best_chromosome.calculate_link_load()
    for link in network.links_list:
        link.number_of_signals = link_load[link.link_id - 1]
        link.number_of_fibers = ceil(link_load[link.link_id - 1] / link.single_module_capacity)
    return network
