from math import ceil

from model import Network, Demand
from solution_checker import check_solution
from random import randint


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
    population_number = 2
    # Solve here
    # TODO add evolutionary algorithm
    check_solution(network)

    # initialisation of population
    population = init_population(population_number, network)
    for idx, chromosome in enumerate(population):
        print('Chromosome: ' + str(idx))
        chromosome.print()
    # initialisation of chromosome fitnesses

    # loop START

    # pairs selection

    # crossover inside pairs(new population init)

    # mutation in new population

    # update population based on fitnesses

    # stopping criterium

    # loop END

    return mock_solution(network)


def init_population(population_number: int, network: Network) -> list:
    chromosomes = []
    for _ in range(0, population_number):
        chromosomes.append(Chromosome(network))
    return chromosomes


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

    @staticmethod
    def init_genes(demands_list: list, paths_number: int) -> list:
        genes = []
        for idx in range(0, len(demands_list)):
            genes.append(Gene(demands_list[idx], paths_number))
        return genes

    def calculate_fitness(self) -> int:
        """
        Calculate chromosome fitness which is the summary cost of all modules for each link in the network. Modules
        number for each link is calculated based on link load.
        """
        fitness = 0
        link_load = self.calculate_link_load()
        for link in self.links_list:
            fitness += ceil(link_load[link.link_id - 1] / link.single_module_capacity) * link.module_cost
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
        self.init_paths_values(demand)

    def init_paths_values(self, demand):
        for demand_path_id in range(0, demand.number_of_demand_paths):
            if demand_path_id == 0:
                self.paths[demand_path_id] = randint(0, demand.demand_volume)
            elif demand_path_id == demand.number_of_demand_paths - 1:
                if demand.number_of_demand_paths > 1:
                    self.paths[demand_path_id] = demand.demand_volume - sum(self.paths[0:demand_path_id])
                else:
                    self.paths[demand_path_id] = demand.demand_volume
            else:
                self.paths[demand_path_id] = randint(0, demand.demand_volume - sum(self.paths[0:demand_path_id]))

    def print(self):
        print(self.paths)
