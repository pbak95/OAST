# input data class
class Demand:
    def __init__(self, demand_id: int, start_node: int, end_node: int, demand_volume: int, number_of_demand_paths: int,
                 demand_path_list: list, solution_number_of_demand_paths=0):
        self.demand_id = demand_id
        self.start_node = int(start_node)  # node id
        self.end_node = int(end_node)  # node id

        # Input variables
        self.demand_volume = int(demand_volume)
        self.number_of_demand_paths = int(number_of_demand_paths)
        if not all(isinstance(n, DemandPath) for n in demand_path_list):
            return 1
        self.demand_path_list = demand_path_list

        # Output variables
        self.solution_number_of_demand_paths = solution_number_of_demand_paths

    def print(self):
        print(f'\tDemand idx: {self.demand_id}')
        print(f'\t\tdemand_volume = {self.demand_volume} Mbps')
        for attr in ('start_node', 'end_node', 'number_of_demand_paths', 'demand_path_list'):
            print(f'\t\t{attr} = {getattr(self, attr)}')

    def print_as_line(self):
        list_as_multiline = "\n".join([x.print_as_line() for x in self.demand_path_list])
        return f'{self.demand_id} {self.solution_number_of_demand_paths}\n{list_as_multiline}\n'


# input data class
class DemandPath:
    def __init__(self, demand_path_id: int, link_list: list, solution_path_signal_count=0):
        # Input variables
        self.demand_path_id = demand_path_id
        self.link_list = link_list

        # Output variables
        self.solution_path_signal_count = solution_path_signal_count

    def __str__(self):
        return f'(demand_path_id = {self.demand_path_id}; link_list = ({self.link_list}))'

    def __unicode__(self):
        return f'(demand_path_id = {self.demand_path_id}; link_list = ({self.link_list}))'

    def __repr__(self):
        return f'(demand_path_id = {self.demand_path_id}; link_list = ({self.link_list}))'

    def print(self):
        for attr in dir(self):
            if attr in ('demand_path_id', 'link_list'):
                print(f'\t\t{attr} = {getattr(self, attr)}')

    def print_as_line(self):
        return f'{self.demand_path_id} {self.solution_path_signal_count}'
