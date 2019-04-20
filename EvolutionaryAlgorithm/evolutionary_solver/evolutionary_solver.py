from model import Network, Link, DemandFlow, DemandPathFlow
from solution_checker import check_solution


def mock_solution():
    number_of_links = 2
    links_load_list = [
        Link(link_id=1, start_node=1, end_node=2, maximum_number_of_modules=4, module_cost=1,
             single_module_capacity=2, number_of_signals=2, number_of_fibers=3),
        Link(link_id=2, start_node=1, end_node=2, maximum_number_of_modules=4, module_cost=1,
             single_module_capacity=2, number_of_signals=2, number_of_fibers=3),
    ]
    number_of_demands = 2
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

    return number_of_links, links_load_list, number_of_demands, demands_flow_list


def evolutionary_solve(network: Network):
    # Solve here
    check_solution(network)

    return mock_solution()
