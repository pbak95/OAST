from model import Network, DemandFlow, DemandPathFlow
from solution_checker import check_solution


def mock_solution(network) -> Network:
    links = network.links_list
    for link in links:
        link.number_of_fibers = 1
        link.number_of_signals = 2

    demands_flow_list = [
        DemandFlow(
            demand_id=1, number_of_demand_paths=1,
            demand_path_flow_list=[DemandPathFlow(path_id=1, path_singal_count=2)]
        ),
        DemandFlow(
            demand_id=2, number_of_demand_paths=1,
            demand_path_flow_list=[DemandPathFlow(path_id=2, path_singal_count=2)]
        )
    ]
    network.demand_solution = demands_flow_list

    return network


def evolutionary_solve(network: Network) -> Network:
    # Solve here
    check_solution(network)

    return mock_solution(network)
