import os
import errno

from model import Link, Demand, Network


def print_values(number_of_links, links_list, number_of_demands, demands_list):
    print(f'Number of links: {number_of_links}')
    print(f'Number of demands: {number_of_demands}')

    for idx, link in enumerate(links_list):
        print(f'\tlink.py idx: {idx}')
        link.print()

    for idx, demand in enumerate(demands_list):
        print(f'\tDemand idx: {idx}')
        demand.print()


def read_links(file) -> (int, list):
    number_of_links = int(file.readline().split()[0])
    # Move pointer to second line
    next(file)

    link_list = []
    # Enumerate uses next to move lines
    for idx, line in enumerate(file):
        values = line.split()

        if len(values) == 1 and values[0] == '-1':
            # Separator found! Links have been read
            return number_of_links, link_list

        link_list.append(Link(values))


def read_demands(file) -> (int, list):
    next(file)
    number_of_demands = int(file.readline().split()[0])
    next(file)
    demands_list = []

    for demand_idx in range(number_of_demands):
        values = file.readline().split()
        start_node = values[0]
        end_node = values[1]
        demand_volume = values[2]
        number_of_demand_paths = int(file.readline().split()[0])

        demand_path_list = []
        for demand_paths_idx in range(number_of_demand_paths):
            path_values = file.readline().split()
            demand_path_id = path_values[0]
            link_list = path_values[1:]
            demand_path_list.append((demand_path_id, link_list))
        demands_list.append(Demand(start_node, end_node, demand_volume, number_of_demand_paths, demand_path_list))
        if demand_idx != number_of_demands - 1:
            next(file)
    return number_of_demands, demands_list


def write_link_part(file, number_of_links, links_load_list):
    file.write(str(number_of_links) + '\n')

    for idx in range(number_of_links):
        file.write(links_load_list[idx].print_result_to_file() + '\n')
    file.write('-1\n')


def write_demand_part(file, number_of_demands, demands_flow_list):
    file.write(str(number_of_demands) + '\n\n')

    for idx in range(number_of_demands):
        file.write(demands_flow_list[idx].print_as_line() + '\n')


def write_file(file_name: str, network: Network):
    if not os.path.exists(os.path.dirname(file_name)):
        try:
            os.makedirs(os.path.dirname(file_name))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(file_name, 'w') as file:
        write_link_part(file, network.number_of_links, network.links_list)
        file.write('\n')
        write_demand_part(file, len(network.demand_solution), network.demand_solution)
