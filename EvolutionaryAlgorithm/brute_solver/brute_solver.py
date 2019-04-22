import copy
import itertools
import math
import time
import sys

from model import Network


def brute_solve(network: Network) -> Network:
    start = time.time()
    print("Bruteforce started!")

    # Get all possible permutations of paths
    possibilities = Possibilities(network)

    iteration = Iteration(possibilities)

    best_solution = Solution(math.inf, [])

    update_progress(0)
    # For every permutation calculate load on links and how many modules are needed to accommodate this load
    # Select best solution - can be multiple ones
    while iteration.next_iteration():
        competing_solution = calculate_modules_cost(network, iteration.values)
        best_solution = best_solution.compare(competing_solution)

    update_progress(1)
    end = time.time()

    print()
    print("Solution:")
    print(best_solution.cost)
    print("Number of possible solutions is {}:".format(len(best_solution.values)))
    for solveNumber in range(len(best_solution.values)):
        best_solution.print(network, solveNumber)

    print("Calculations took: {}".format(end - start))

    for demand in range(len(best_solution.values[0])):
        for path in range(len(best_solution.values[0][0])):
            try:
                network.demands_list[demand].demand_path_list[path].solution_path_signal_count = best_solution.values[0][demand][path]
            except IndexError:
                # Should be only printed in debug
                print("IndexError number of paths for demand {} is shorter then max {}".format(demand, network.longest_demand_path))

    network.update_link_capacity()
    return network


class Solution(object):
    def __init__(self, cost: float, values: []):
        self.cost = cost
        self.values = values

    def compare(self, other):
        if other.cost < self.cost:
            print(other.cost, end=" ")
            return other
        elif other.cost == self.cost:
            self.append(other.values[0])
            return self
        else:
            return self

    def append(self, new_solution: []):
        self.values.append(new_solution)

    def print(self, network: Network, solve_number: int):

        row_format = "{:<7}" + "{:^5}" * network.number_of_demands
        demand_list = ["[%s]" % x for x in range(1, network.number_of_demands + 1)]
        path_list = ["[%s]" % x for x in range(1, network.longest_demand_path + 1)]
        transposed_data = zip(*self.values[solve_number])

        print('Routes: \\ Demands:')
        print(row_format.format("", *demand_list))
        for path_id, row in enumerate(transposed_data):
            print(row_format.format(path_list[path_id], *row))
        print(row_format.format("h(d):",
                                *[network.demands_list[x].demand_volume for x in range(len(network.demands_list))]))
        print("Is solution valid: {}".format(self.validate(network, solve_number)))
        print()

    def validate(self, network: Network, solve_number: int):
        valid = True
        for demand in range(len(self.values[solve_number])):
            demand_passed = sum(self.values[solve_number][demand])
            valid = valid and (demand_passed >= network.demands_list[demand].demand_volume)

        return valid


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


class Iteration(object):

    def __init__(self, possibilities: Possibilities):
        self.possibilities = possibilities
        self.values = []
        self.state = [0] * self.possibilities.number_of_demands
        for i in range(0, self.possibilities.number_of_demands):
            self.values.append([0] * self.possibilities.longest_route)

    def next_iteration(self):
        for i in reversed(range(0, self.possibilities.number_of_demands)):
            # Very important '- 1' here
            if self.state[i] < len(self.possibilities[i]) - 1:
                self.state[i] = self.state[i] + 1
                self.set_values()
                return True
            elif self.state[i - 1] < len(self.possibilities[i - 1]) - 1:
                self.state[i - 1] = self.state[i - 1] + 1
                self.state[i:] = [0] * (self.possibilities.number_of_demands - i)
                if i == 1:
                    update_progress(self.state[0] / len(self.possibilities[0]))
                self.set_values()
                return True
        return False

    def set_values(self):
        for i in range(0, self.possibilities.number_of_demands):
            self.values[i] = self.possibilities[i][self.state[i]]


class PathIteration(object):

    def find_combinations_util(self, arr, index, buckets, num,
                               reduced_num, output):

        # Base condition
        if reduced_num < 0:
            return

        # If combination is
        # found, print it
        if reduced_num == 0:
            curr_array = [0] * buckets
            curr_array[:index] = arr[:index]
            all_perm = list(itertools.permutations(curr_array))
            for solution in set(all_perm):
                output.append(solution)
            return

            # Find the previous number stored in arr[].
        # It helps in maintaining increasing order
        prev = 1 if (index == 0) else arr[index - 1]

        # note loop starts from previous
        # number i.e. at array location
        # index - 1
        for k in range(prev, num + 1):
            # Found combination would take too many buckets
            if index >= buckets:
                return
            # next element of array is k
            arr[index] = k

            # call recursively with
            # reduced number
            self.find_combinations_util(arr, index + 1, buckets, num,
                                        reduced_num - k, output)

            # Function to find out all

    # combinations of positive numbers
    # that add upto given number.
    # It uses findCombinationsUtil()
    def find_combinations(self, n, buckets):

        output = []
        # array to store the combinations
        # It can contain max n elements
        arr = [0] * buckets

        # find all combinations
        self.find_combinations_util(arr, 0, buckets, n, n, output)
        return output


def calculate_modules_cost(network, flow_array) -> Solution:
    modules_cost = 0
    load = calculate_links_load(network, flow_array)
    for linkId in range(0, network.number_of_links):
        link = network.links_list[linkId]
        # Check if link is not overloaded
        if load[linkId] < link.maximum_number_of_modules * link.single_module_capacity:
            modules_used = math.ceil(load[linkId] / link.single_module_capacity)
            modules_cost = modules_cost + modules_used * link.module_cost
    return Solution(modules_cost, [copy.deepcopy(flow_array)])


def calculate_links_load(network, flow_array):
    load = [0] * network.number_of_links
    for demand in range(0, network.number_of_demands):
        for path in range(0, network.demands_list[demand].number_of_demand_paths):
            flows_running_this_path = flow_array[demand][path]
            for linkInPath in network.demands_list[demand].demand_path_list[path].link_list:
                load[linkInPath - 1] = load[linkInPath - 1] + flows_running_this_path
    return load


# Displays or updates a console progress bar
def update_progress(progress):
    bar_length = 100
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(bar_length*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(bar_length-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()
