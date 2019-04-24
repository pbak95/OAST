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
    population_number = 10
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

    @staticmethod
    def init_genes(demands_list: list, paths_number: int) -> list:
        genes = []
        for idx in range(0, len(demands_list)):
            genes.append(Gene(demands_list[idx], paths_number))
        return genes

    def print(self):
        for gene in self.genes:
            gene.print()


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
