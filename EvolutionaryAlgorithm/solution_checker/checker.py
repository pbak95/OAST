from model import Network


def check_solution(network: Network) -> bool:
    # TODO write demands checker
    total_link_cost = 0
    for link in network.links_list:
        # Minimalize total link cost
        total_link_cost = total_link_cost + link.number_of_fibers * link.module_cost

        link_capacity = link.single_module_capacity * link.number_of_fibers

        link_used_capacity = link.single_module_capacity * link.number_of_signals
        # checking demands
        for demand_flow in network.demand_solution:
            demand_id = demand_flow.demand_id
            demand = [item for item in network.demands_list if item.demand_id == demand_id]

            for demand_path in demand.demand_path_list:
                pass

    pass
