# input data class
class Network:
    def __init__(self, number_of_links: int, links_list: list, number_of_demands: int,
                 demands_list: list, demand_solution=None):
        """

        :param number_of_links: len(links_list)
        :param links_list: Network links list, links contain input and output variables
        :param number_of_demands: len(demands_list)
        :param demands_list: Network demands list, demands contain input and output variables
        :param demand_solution:
        """
        self.number_of_links = number_of_links
        self.links_list = links_list
        self.number_of_demands = number_of_demands
        self.demands_list = demands_list

    def print(self):
        print('### INPUT ###')
        print(f'Number of links: {self.number_of_links}')
        print(f'Number of demands: {self.number_of_demands}')

        for _, link in enumerate(self.links_list):
            link.print()

        for _, demand in enumerate(self.demands_list):
            demand.print()

    def get_all_possible_demands_of_link(self, link_id) -> list:
        result = []
        for demand in self.demands_list:
            for path in demand.demand_path_list:
                if link_id in path.link_list:
                    result.append((demand.demand_id, path.demand_path_id))
        return result

    def update_link_capacity(self):
        for link in self.links_list:
            link.number_of_signals = 0
            link.number_of_fibers = 0
            for demand in self.demands_list:
                for path in demand.demand_path_list:
                    if link.link_id in path.link_list and path.solution_path_signal_count != 0:
                        link.number_of_signals = link.number_of_signals + 1
                        link.number_of_fibers = link.single_module_capacity * path.solution_path_signal_count
