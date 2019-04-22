import copy
import itertools
import math
import time
import sys

from model import Network

FALSE_START = False


def brute_solve(network: Network) -> Network:
    start = time.time()
    print("Bruteforce started!")

    # Get all possible permutations of paths
    possibilities = []
    for demand in network.demands_list:
        path_iter = PathIteration()
        possibilities.append(path_iter.find_combinations(demand.demand_volume, demand.number_of_demand_paths))

    # Initialize variables
    iteration = Iteration(possibilities)
    if FALSE_START:
        iteration.state[0] = 9
    best_solution = math.inf
    best_solution_values = []

    # For every permutation calculate load on links and how many modules are needed to accommodate this load
    # Select best solution - can be multiple
    while iteration.next_iteration():
        module_cost = calculate_modules_cost(network, iteration.values)

        if module_cost < best_solution:
            # Print current best solution
            print(module_cost, end=" ")
            best_solution = module_cost
            best_solution_values = [copy.deepcopy(iteration.values)]
        elif module_cost == best_solution:
            best_solution_values.append(copy.deepcopy(iteration.values))

    update_progress(1)
    end = time.time()

    if best_solution == 0:
        print("Something went wrong!")
        exit(-1)

    # Printing
    print()
    print("Solution:")
    print(best_solution)
    print("Number of possible solutions is {}:".format(len(best_solution_values)))
    for solve in best_solution_values:
        print_fucked_up_array(network, solve)

    print("Calculations took: {}".format(end - start))

    network.update_link_capacity()
    return network


def calculate_modules_cost(network, flow_array):
    modules_cost = 0
    load = calculate_links_load(network, flow_array)
    for linkId in range(0, network.number_of_links):
        link = network.links_list[linkId]
        # Check if link is not overloaded
        if load[linkId] < link.maximum_number_of_modules * link.single_module_capacity:
            modules_used = math.ceil(load[linkId] / link.single_module_capacity)
            modules_cost = modules_cost + modules_used * link.module_cost
    return modules_cost


def calculate_links_load(network, flow_array):
    load = [0] * network.number_of_links
    for demand in range(0, network.number_of_demands):
        for path in range(0, network.demands_list[demand].number_of_demand_paths):
            flows_running_this_path = flow_array[demand][path]
            for linkInPath in network.demands_list[demand].demand_path_list[path].link_list:
                load[linkInPath - 1] = load[linkInPath - 1] + flows_running_this_path
    return load


def validate(network, solution):
    valid = True
    for demand in range(0, len(solution)):
        demand_passed = sum(solution[demand])
        valid = valid and (demand_passed >= network.demands_list[demand].demand_volume)

    return valid


def get_longest_route_in_possibilities(possibility_array):
    output = 0
    for demandPossibilities in possibility_array:
        for possibility in demandPossibilities:
            if len(possibility) > output:
                output = len(possibility)
    return output


class Iteration(object):

    def __init__(self, possibilities):
        self.numberOfDemands = len(possibilities)
        self.possibilities = possibilities
        self.longestPath = get_longest_route_in_possibilities(possibilities)
        self.values = []
        self.state = [0] * self.numberOfDemands
        for i in range(0, self.numberOfDemands):
            self.values.append([0] * self.longestPath)

    def next_iteration(self):
        for i in reversed(range(0, self.numberOfDemands)):
            # Very important '- 1' here
            if self.state[i] < len(self.possibilities[i]) - 1:
                self.state[i] = self.state[i] + 1
                self.set_values()
                return True
            elif self.state[i - 1] < len(self.possibilities[i - 1]) - 1:
                self.state[i - 1] = self.state[i - 1] + 1
                self.state[i:] = [0] * (self.numberOfDemands - i)
                if i == 1:
                    update_progress(self.state[0] / len(self.possibilities[0]))
                self.set_values()
                return True
        return False

    def set_values(self):
        for i in range(0, self.numberOfDemands):
            # Why there was -1 ?
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


# Lets hide this func so nobody will see it
def print_fucked_up_array(network, array):
    print()
    print('Routes: \\ Demands:')
    print("", end='\t\t')
    for demand in range(0, len(array)):
        print("[{}]".format(demand), end='\t')
    print()
    print()
    for path in range(0, len(array[0])):
        print("[{}]".format(path), end='\t\t')
        for demad in range(0, len(array)):
            try:
                value = array[demad][path]
                network.demands_list[demad].demand_path_list[path].solution_path_signal_count = int(value)
            except IndexError:
                value = " "

            print(value, end='\t')
        print()
    print()
    print("h(d):", end='\t\t')
    for demand in range(0, len(array)):
        print(network.demands_list[demand].demand_volume, end='\t')
    print()
    print("Is solution valid: {}".format(validate(network, array)))


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
