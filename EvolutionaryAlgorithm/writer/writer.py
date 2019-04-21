import os
import errno

from model import Network


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
        write_demand_part(file, len(network.demands_list), network.demands_list)
