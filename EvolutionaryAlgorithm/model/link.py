# input data class
class Link:
    def __init__(self, link_id: int, start_node: int, end_node: int,
                 maximum_number_of_modules: int, module_cost: float,
                 single_module_capacity: int, number_of_signals=0, number_of_fibers=0):
        """
        Constructor
        :param link_id: Unique id
        :param start_node: Node id
        :param end_node: Node id
        :param maximum_number_of_modules:
        How much modules could fit in this link
        :param module_cost: Single module cost in abstract units
        :param single_module_capacity: Mbps of single module
        :param number_of_signals: Solution variable
        (how much demands path is using this link)
        :param number_of_fibers: Solution variable
        (how much modules are used) < maximum_number_of_modules
        """
        self.link_id = link_id
        self.start_node = start_node
        self.end_node = end_node

        # input variables
        self.maximum_number_of_modules = maximum_number_of_modules
        self.module_cost = module_cost
        self.single_module_capacity = single_module_capacity

        # output variables
        self.number_of_signals = number_of_signals
        self.number_of_fibers = number_of_fibers

    def print(self):
        print(f'\tLink idx: {self.link_id}')
        for attr in ('start_node', 'end_node', 'maximum_number_of_modules',
                     'module_cost', 'single_module_capacity'):
            print(f'\t\t{attr} = {getattr(self, attr)}')

    def print_result(self):
        print(f'\tLink idx: {self.link_id}')
        for attr in ('start_node', 'end_node', 'number_of_signals'):
            print(f'\t\t{attr} = {getattr(self, attr)}')
        print(f'\t\tnumber_of_fibers = {self.number_of_fibers} x {self.single_module_capacity} Mbps')

    def print_result_to_file(self):
        return f'{self.link_id} {self.number_of_signals} {self.number_of_fibers}'

