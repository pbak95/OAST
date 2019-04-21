from model import Network
from solution_checker import check_solution


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


def brute_solve(network: Network) -> Network:
    # Solve here
    # TODO add brute force algorithm
    check_solution(network)

    return mock_solution(network)
