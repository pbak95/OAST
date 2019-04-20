class Demand:
    def __init__(self, start_node, end_node, demand_volume, number_of_demand_paths, demand_path_list):
        self.start_node = int(start_node) # node id
        self.end_node = int(end_node) # node id
        self.demand_volume = int(demand_volume)
        self.number_of_demand_paths = int(number_of_demand_paths)
        self.demand_path_list = demand_path_list

    def print(self):
        for attr in dir(self):
            if attr in ('start_node', 'end_node', 'demand_volume', 'number_of_demand_paths', 'demand_path_list'):
                print(f'\t\t{attr} = {getattr(self, attr)}')
