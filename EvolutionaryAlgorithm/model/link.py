# input data class
class Link:
    def __init__(self, link_id: int, start_node: int, end_node: int, demand_volume: int, module_cost: float,
                 link_module_capacity: int):
        self.link_id = link_id
        self.start_node = start_node
        self.end_node = end_node
        self.demand_volume = demand_volume
        self.module_cost = module_cost
        self.link_module_capacity = link_module_capacity

    def print(self):
        print(f'\tLink idx: {self.link_id}')
        for attr in dir(self):
            if attr in ('start_node', 'end_node', 'number_of_modules', 'module_cost', 'link_module'):
                print(f'\t\t{attr} = {getattr(self, attr)}')


# output data class
class LinkLoad:
    def __init__(self, link_id: int, number_of_signals: int, number_of_fibers: int):
        self.link_id = link_id
        self.number_of_signals = number_of_signals
        self.number_of_fibers = number_of_fibers

    def print_as_line(self):
        return f'{self.link_id} {self.number_of_signals} {self.number_of_fibers}'

    def print(self):
        print(f'\tLink idx: {self.link_id}')
        for attr in dir(self):
            if attr in ('number_of_signals', 'number_of_fibers'):
                print(f'\t\t{attr} = {getattr(self, attr)}')
