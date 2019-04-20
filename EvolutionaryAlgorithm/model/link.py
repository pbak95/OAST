class Link:
    def __init__(self, values):
        if len(values) != 5:
            return 1
        self.start_node = int(values[0]) # node id
        self.end_node = int(values[1]) # node id
        self.demand_volume = int(values[2])
        self.module_cost = float(values[3])
        self.link_module = int(values[4])

    def print(self):
        for attr in dir(self):
            if attr in ('start_node', 'end_node', 'number_of_modules', 'module_cost', 'link_module'):
                print(f'\t\t{attr} = {getattr(self, attr)}')
