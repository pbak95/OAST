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
    mutation_counter = 0
    start = time.time()
    total_time = None

    while True:

        print("GENERATION: ", i)
        for o in population:
            o.update_fitness()
        # print only first element
        population[0].print()

        # pairs selection
        pairs = select_pairs_rulette(population)
        new_population = make_crossover(pairs)

        # mutation in new population
        for chromosome in new_population:
            if chromosome.mutate(mutation_probability):
                mutation_counter += 1

        # set next population parents based on current population and their childes
        population = sorted(sorted(new_population + population)[0:population_size])

        # print("NEW POPULATION:")
        # population[0].print()

        # stopping criterium
        if config.stop == 'best_iter':
            if i > 0 and i % config.stop_arg == 0:
                if best_chromosome.fitness == population[0].fitness and population[0].network.is_valid():
                    end = time.time()
                    total_time = end - start
                    print_best_solution(best_chromosome, i, 'BEST ITERATION', mutation_counter, total_time)
                    break

            if i % config.stop_arg == 0:
                best_chromosome = population[0]
        elif config.stop == 'iter':
            best_chromosome = population[0]
            if i == config.stop_arg:
                end = time.time()
                total_time = end - start
                print_best_solution(best_chromosome, i, 'NUMBER OF ITERATIONS', mutation_counter, total_time)
                break
        elif config.stop == 'mut':
            best_chromosome = population[0]
            if mutation_counter >= config.stop_arg:
                end = time.time()
                total_time = end - start
                print_best_solution(best_chromosome, i, 'MINIMUM NUMBER OF MUTATIONS {}, PERFORMED {}'.format(
                    config.stop_arg, mutation_counter), mutation_counter, total_time)
                break
        elif config.stop == 'time':
            best_chromosome = population[0]
            end = time.time()
            time_interval = end - start
            if time_interval >= config.stop_arg:
                total_time = time_interval
                print_best_solution(best_chromosome, i, 'MINIMUM ELAPSED TIME {} s, TAKES {} s'.format(
                    config.stop_arg, time_interval), mutation_counter, total_time)
                break
        elif config.stop == 'valid':
            best_chromosome = population[0]
            if best_chromosome.network.is_valid():
                end = time.time()
                total_time = end - start
                print_best_solution(best_chromosome, i, 'VALID RESULT', mutation_counter, total_time)
                break
        i += 1

    result_network = update_network_link_parameters(best_chromosome, network)
    for link in result_network.links_list:
        link.print_result()
    return result_network


def print_best_solution(chromosome, iter, stop, mutations_number, time):
    print('STOPPING CRITERIUM ACHIEVED: ', stop)
    print('BEST SOLUTION IN ITERATION: ', iter)
    print('Mutations number: ', mutations_number)
    print('Elapsed time: ', time)
    chromosome.print()

def init_population(population_number: int, network: Network) -> list:
    chromosomes = []
    for _ in range(0, population_number):
        chromosomes.append(Chromosome(network))
    return sorted(chromosomes)


def select_pairs(population: list) -> list:
    pairs = []

    # for _ in range(0, math.floor(len(population) / 2) - 1):
    #     first_idx = randint(0, len(population) - 1)
    #     first_parent = population.pop(first_idx)
    #     second_idx = randint(0, len(population) - 1)
    #     second_parent = population.pop(second_idx)
    #     pairs.append((first_parent, second_parent))
    #
    # return pairs
    return list(zip(population[::2], population[1::2]))

def select_pairs_rulette(population: list) -> list:
    pairs = []
    scaled_fitnesses = []
    sections = []
    parts = []
    worst_fitness = population[len(population) - 1].fitness
    population_max_idx = len(population) - 1
    for idx, chromosome in enumerate(population):
        diff = max(worst_fitness - chromosome.fitness, 1)
        scaled_fitnesses.append(diff)
        if diff not in parts:
            parts.append(diff)
            sections.append((diff, idx))
    parts_sum = sum(parts)
    for idx, section in enumerate(sections):
        sections[idx] = (section[0] / parts_sum, section[1])

    for idx, section in enumerate(sections):
        if idx > 0:
            sections[idx] = (section[0] + sections[idx - 1][0], section[1])

    for _ in range(0, math.floor(len(population) / 2)):
        first_parent_number = random()
        second_parent_number = random()
        first_parent = None
        second_parent = None
        for idx, section in enumerate(sections):
            if first_parent_number <= section[0] and first_parent is None:
                first_parent = population[getIndex(idx, sections, section, population_max_idx)]
            if second_parent_number <= section[0] and second_parent is None:
                second_parent = population[getIndex(idx, sections, section, population_max_idx)]
            if first_parent is not None and second_parent is not None: break
        pairs.append((first_parent, second_parent))
    return pairs


def getIndex(idx, sections, section, population_max_idx) -> int:
    if idx == 0:
        return randint(0, section[1])
    elif idx == len(sections) - 1:
        return randint(section[1], population_max_idx)
    else:
        return randint(section[1], sections[idx + 1][1] - 1)


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
        self.network = network
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
        # print(link_load)
        for link in self.links_list:
            modules_number = ceil(link_load[link.link_id - 1] / link.single_module_capacity)
            if modules_number > link.maximum_number_of_modules:
                fitness += link_load[link.link_id - 1] + link_load[link.link_id - 1] - (link.maximum_number_of_modules * link.single_module_capacity)
            else:
                fitness += link_load[link.link_id - 1]
        # print(fitness)
        return fitness

    def calculate_link_load(self) -> list:
        """
        Calculate link load on the basis of demand volume for each demand path
        :return: list of link load for each link where load index is equal (link_id - 1)
        """
        load = [0] * self.number_of_links
        for real_link in self.links_list:
            real_link.number_of_signals = 0
            real_link.number_of_fibers = 0
        for demand in range(0, self.number_of_demands):
            for path in range(0, self.demands_list[demand].number_of_demand_paths):
                flows_running_this_path = self.genes[demand].paths[path]
                for linkInPath in self.demands_list[demand].demand_path_list[path].link_list:
                    load[linkInPath - 1] = load[linkInPath - 1] + flows_running_this_path
                    for real_link in self.links_list:
                        if real_link.link_id == linkInPath:
                            real_link.number_of_signals = real_link.number_of_signals + flows_running_this_path
                            real_link.number_of_fibers = math.ceil(load[linkInPath - 1]/real_link.single_module_capacity)
        return load

    def print(self):
        self.network.update_link_capacity()
        self.print_link_load()
        print('Fitness: ', self.fitness)
        # for gene in self.genes:
        #     gene.print()
        print('\n')

    def print_link_load(self):
        load_list = self.calculate_link_load()
        result_string = ""
        for idx, load in enumerate(load_list):
            result_string += str(load) + ":" + str(self.network.links_list[idx].number_of_fibers) + " , "
        print('Link load: ', result_string)
        print('Correctness: ', self.network.is_valid())


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
        # self.init_paths_values_idx()

    def init_paths_values(self):
        if self.demand.number_of_demand_paths == 1:
            self.paths[0] = self.demand.demand_volume
        else:
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

    def init_paths_values_idx(self):
        for _ in range(0, self.demand.demand_volume):
            rand_path_idx = randint(0, self.demand.number_of_demand_paths - 1)
            self.paths[rand_path_idx] += 1

    def mutate(self):
        path_idx1 = 0
        while True:
            path_idx1 = randint(0, self.demand.number_of_demand_paths - 1)
            if self.paths[path_idx1] != 0: break
        path_idx2 = randint(0, self.demand.number_of_demand_paths - 1)
        self.paths[path_idx1] -= 1
        self.paths[path_idx2] += 1

    def print(self):
        print(self.paths)


def update_network_link_parameters(best_chromosome: Chromosome, network: Network) -> Network:
    link_load = best_chromosome.calculate_link_load()
    for link in network.links_list:
        link.number_of_signals = link_load[link.link_id - 1]
        link.number_of_fibers = ceil(link_load[link.link_id - 1] / link.single_module_capacity)
    return network
