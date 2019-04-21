import copy
import itertools
import time

from model import Network, DemandFlow, DemandPathFlow
from solution_checker import check_solution
import math


def mock_solution(network) -> Network:
    links = network.links_list
    for link in links:
        link.number_of_fibers = 1
        link.number_of_signals = 2

    # demands_flow_list = [
    #     DemandFlow(
    #         demand_id=1, number_of_demand_paths=1,
    #         demand_path_flow_list=[DemandPathFlow(path_id=1, path_singal_count=2)]
    #     ),
    #     DemandFlow(
    #         demand_id=2, number_of_demand_paths=1,
    #         demand_path_flow_list=[DemandPathFlow(path_id=2, path_singal_count=2)]
    #     )
    # ]
    # network.demand_solution = demands_flow_list

    return network


def brute_solve(network: Network) -> Network:
    # print(network.demands_list[0].demand_id)
    # f = math.inf
    # n = 1000
    #
    # x = [0] * n
    #
    # for a in range(1, n):
    #     for b in range(x[a], network.demands_list - sum(x[:a])):
    longestRoute = 0
    for demand in network.demands_list:
        if longestRoute < getLongestRouteInDemand(demand):
            longestRoute = getLongestRouteInDemand(demand)
    print(longestRoute)

    maxPathsCapacity = []
    for i in range(0, len(network.demands_list)):
        maxPathsCapacity.append([0] * longestRoute)

    print(maxPathsCapacity)
    for demand in network.demands_list:
        for route in demand.demand_path_list:
            # Why route.demand_path_id is a string?
            maxPathsCapacity[demand.demand_id - 1][int(route.demand_path_id) - 1] = mininalDemandOnPath(network, route)

    myNetwork = copy.deepcopy(network)

    print(maxPathsCapacity)
    printFuckedUpArray(network, maxPathsCapacity)
    print("Is solution valid:")
    print(validate(network, maxPathsCapacity))

    check_solution(network)

    start = time.time()

    # while iteration.nextIteration():
    #     for link in range(0, len(myNetwork.links_list)):
    #         myNetwork.links_list[link].maximum_number_of_modules = iteration.values[link]
    #         for demand in network.demands_list:
    #             for route in demand.demand_path_list:
    #                 # Why route.demand_path_id is a string?
    #                 maxPathsCapacity[demand.demand_id - 1][int(route.demand_path_id) - 1] = mininalDemandOnPath(myNetwork,
    #                                                                                                             route)
    #         printFuckedUpArray(myNetwork, maxPathsCapacity)
        # pass
        # print(iteration.values)

    possibilities = []
    for demand in network.demands_list:
        pathIter = PathIteration()
        possibilities.append(pathIter.findCombinations(demand.demand_volume, demand.number_of_demand_paths));

    print(possibilities)
    iteration = Iteration(possibilities)

    bestSolution = math.inf
    bestSolutionValues = []
    iteration.nextIteration()
    # print(iteration.values)
    while iteration.nextIteration():
        moduleCost = calculateModulesCost(network, iteration.values)

        if moduleCost < bestSolution:
            print(moduleCost, end=" ")
            # print(iteration.values, end=" ")
            bestSolution = moduleCost
            bestSolutionValues = [copy.deepcopy(iteration.values)]
        elif moduleCost == bestSolution:
            bestSolutionValues.append(copy.deepcopy(iteration.values))

            # pass
    # c = [(2, 1, 0), (4, 0, 0), (5, 0), (1, 1, 0), (3, 0, 0), (4, 0, 0)]
    # moduleCost = calculateModulesCost(network, c)
    # print(moduleCost)
    # b = [(0, 0, 3), (4, 0, 0), (5, 0), (2, 0, 0), (0, 0, 3), (4, 0, 0)]
    # moduleCost = calculateModulesCost(network, b)
    # print(moduleCost)

    # n = 4;
    # pathIter = PathIteration(2, 2)
    # pathIter.findCombinations(n, 3);
    print("Solution:")
    print(bestSolution)
    print(bestSolutionValues)

    end = time.time()
    print(end - start)

    return mock_solution(network)


def calculateModulesCost(network, flowArray):
    modulesCost = 0
    load = calculateLinksLoad(network, flowArray)
    for linkId in range(0, network.number_of_links):
        link = network.links_list[linkId]
        # Check if in capacity
        if load[linkId] < link.maximum_number_of_modules * link.single_module_capacity:
            modulesUsed = math.ceil(load[linkId] / link.single_module_capacity)
            modulesCost = modulesCost + modulesUsed * link.module_cost
    return modulesCost
    # print(load)
    # numberOfModules = 0
    # load = []
    # for i in range(0, network.number_of_demands):
    #     load.append([0] * self.longestPath)
    # for demand in range(0, network.number_of_demands):
    #     for path in range(0, network.demands_list[demand].number_of_demand_paths):
    #         flowsRunningThisPath = flowArray[demand][path]


def calculateLinksLoad(network, flowArray):
    load = [0] * network.number_of_links
    for demand in range(0, network.number_of_demands):
        for path in range(0, network.demands_list[demand].number_of_demand_paths):
            flowsRunningThisPath = flowArray[demand][path]
            for linkInPath in network.demands_list[demand].demand_path_list[path].link_list:
                load[linkInPath - 1] = load[linkInPath - 1] + flowsRunningThisPath
    return load


def mininalDemandOnPath(network, route):
    output = math.inf
    for link in route.link_list:
        if network.links_list[link - 1].maximum_number_of_modules < output:
            output = network.links_list[link - 1].maximum_number_of_modules * network.links_list[
                link - 1].single_module_capacity
    return output


def getLongestRouteInDemand(demad):
    output = 0
    for path in demad.demand_path_list:
        if len(path.link_list) > output:
            output = len(path.link_list)
    return output


def printFuckedUpArray(network, array):
    print()
    print('Routes: \\ Demands:')
    print("\t", end='')
    for demand in range(0, len(array)):
        print("\t[" + str(demand) + "]", end='')
    print()
    print()
    for x in range(0, len(array[0])):
        print("[" + str(x) + "]\t", end='')
        for y in range(0, len(array)):
            print("\t" + str(array[y][x]), end='')
        print()
    print()
    print("h(d):", end='')
    for demand in range(0, len(array)):
        print("\t" + str(network.demands_list[demand].demand_volume), end='')

    print()


def validate(network, solution):
    valid = True
    for demand in range(0, len(solution)):
        demandPassed = sum(solution[demand])
        valid = valid and (demandPassed > network.demands_list[demand].demand_volume)

    return valid


class Iteration(object):

    def __init__(self, possibilities):
        self.numberOfDemands = len(possibilities)
        self.possibilities = possibilities
        self.longestPath = self.getLongestRouteInPossibilities(possibilities)
        # print(self.longestPath)
        # self.possibilitiesNumber = 0
        # self.possibilitiesNumber = 0
        self.values = []
        self.state = [0] * self.numberOfDemands
        for i in range(0, self.numberOfDemands):
            self.values.append([0] * self.longestPath)

    def getLongestRouteInPossibilities(self, possibilityArray):
        output = 0
        for demandPossibilities in possibilityArray:
            for possibility in demandPossibilities:
                if len(possibility) > output:
                    output = len(possibility)
        return output


    def nextIteration(self):
        for i in reversed(range(0, self.numberOfDemands)):
            # Very important '- 1' here
            if self.state[i] < len(self.possibilities[i]) - 1:
                self.state[i] = self.state[i] + 1
                self.setValues()
                return True
            elif self.state[i - 1] < len(self.possibilities[i - 1])- 1:
                self.state[i - 1] = self.state[i - 1] + 1
                self.state[i:] = [0] * (self.numberOfDemands - i)
                if i == 1:
                    print('{} %'.format(self.state[0] / len(self.possibilities[0]) * 100))
                self.setValues()
                return True
        return False

    def setValues(self):
        for i in range(0, self.numberOfDemands):
            self.values[i] = self.possibilities[i][self.state[i] - 1]
        # print(self.state)

class PathIteration(object):

    def findCombinationsUtil(self, arr, index, buckets, num,
                             reducedNum, output):

        # Base condition
        if (reducedNum < 0):
            return;

        # If combination is
        # found, print it
        if (reducedNum == 0):
            currArray = [0] * buckets
            currArray[:index] = arr[:index]
            allPerm = list(itertools.permutations(currArray))
            # print(set(allPerm));
            for solution in set(allPerm):
                output.append(solution)
            # for i in range(index):
            #     print(arr[i], end=" ");
            # print("");
            return;

            # Find the previous number stored in arr[].
        # It helps in maintaining increasing order
        prev = 1 if (index == 0) else arr[index - 1];

        # note loop starts from previous
        # number i.e. at array location
        # index - 1
        for k in range(prev, num + 1):
            # Found combination would take too many buckets
            if index >= buckets:
                return
            # next element of array is k
            arr[index] = k;

            # call recursively with
            # reduced number
            self.findCombinationsUtil(arr, index + 1, buckets, num,
                                 reducedNum - k, output);

            # Function to find out all

    # combinations of positive numbers
    # that add upto given number.
    # It uses findCombinationsUtil()
    def findCombinations(self, n, buckets):

        output = []
        # array to store the combinations
        # It can contain max n elements
        arr = [0] * buckets

        # find all combinations
        self.findCombinationsUtil(arr, 0, buckets, n, n, output);
        print(output)
        print(len(output))
        return output