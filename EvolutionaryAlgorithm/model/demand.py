# input data class
class Demand:
    def __init__(self, demand_id: int, start_node: int, end_node: int, demand_volume: int, number_of_demand_paths: int,
                 demand_path_list: list):
        self.demand_id = demand_id
        self.start_node = int(start_node) # node id
        self.end_node = int(end_node) # node id
        self.demand_volume = int(demand_volume)
        self.number_of_demand_paths = int(number_of_demand_paths)
        self.demand_path_list = demand_path_list

    def print(self):
        print(f'\tDemand idx: {self.demand_id}')
        for attr in dir(self):
            if attr in ('start_node', 'end_node', 'demand_volume', 'number_of_demand_paths', 'demand_path_list'):
                print(f'\t\t{attr} = {getattr(self, attr)}')


# input data class
class DemandPath:
    def __init__(self, demand_path_id: int, link_list: list):
        self.demand_path_id = demand_path_id
        self.link_list = link_list

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


# output data class
class DemandFlow:
    def __init__(self, demand_id: int, number_of_demand_paths: int, demand_path_flow_list: list):
        self.demand_id = demand_id
        self.number_of_demand_paths = number_of_demand_paths
        self.demand_path_flow_list = demand_path_flow_list # DemandPathFlow list

    def print_as_line(self):
        list_as_multiline = "\n".join([x.print_as_line() for x in self.demand_path_flow_list])
        return f'{self.demand_id} {self.number_of_demand_paths}\n{list_as_multiline}\n'


# output data class
class DemandPathFlow:
    def __init__(self, path_id: int, path_singal_count: int):
        self.path_id = path_id
        self.path_singal_count = path_singal_count

    def __str__(self):
        return f'({self.path_id} {self.path_singal_count})'

    def __unicode__(self):
        return f'({self.path_id} {self.path_singal_count})'

    def __repr__(self):
        return f'({self.path_id} {self.path_singal_count})'

    def print_as_line(self):
        return f'{self.path_id} {self.path_singal_count}'
