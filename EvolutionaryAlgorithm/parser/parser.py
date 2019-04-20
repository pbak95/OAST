from model import Link, Demand, DemandPath

from model import Network


def read_links(file) -> (int, list):
    number_of_links = int(file.readline().split()[0])
    # Move pointer to second line

    link_list = []
    # Enumerate uses next to move lines
    for idx, line in enumerate(file):
        values = line.split()

        if len(values) == 1 and values[0] == '-1':
            # Separator found! Links have been read
            return number_of_links, link_list

        link_list.append(
            Link(idx + 1, int(values[0]), int(values[1]), int(values[2]), float(values[3]), int(values[4]))
        )


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
            link_list = list(map(int, path_values[1:]))
            demand_path_list.append(DemandPath(demand_path_id, link_list))
        demands_list.append(
            Demand(demand_idx + 1, start_node, end_node, demand_volume, number_of_demand_paths, demand_path_list)
        )
        if demand_idx != number_of_demands - 1:
            next(file)
    return number_of_demands, demands_list


def read_file(file_name: str) -> Network:
    with open(file_name, 'r') as file:
        number_of_links, links_list = read_links(file)
        number_of_demands, demands_list = read_demands(file)
    return Network(number_of_links, links_list, number_of_demands, demands_list)
