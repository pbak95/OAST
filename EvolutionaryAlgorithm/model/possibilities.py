from .network import Network
from .path_iteration import PathIteration


class Possibilities(object):
    def __init__(self, network: Network):
        self.possibilities = []
        for demand in network.demands_list:
            path_iter = PathIteration()
            iter_for_demand = path_iter.find_combinations(demand.demand_volume, demand.number_of_demand_paths)
            for id, perm in enumerate(iter_for_demand):
                # Fill with -1 if any path is shorter than the longest
                if len(perm) < network.longest_demand_path:
                    new_tuple = perm + tuple([0] * (network.longest_demand_path - len(perm)))
                    iter_for_demand[id] = new_tuple
            self.possibilities.append(iter_for_demand)

        self.number_of_demands = len(self.possibilities)
        self.longest_route = network.longest_demand_path

    def __getitem__(self, y):
        return self.possibilities[y]
