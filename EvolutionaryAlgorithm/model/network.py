# input data class
class Network:
    def __init__(self, number_of_links: int, links_list: list, number_of_demands: int, demands_list: list,
                 demand_solution=[]):
        self.number_of_links = number_of_links
        self.links_list = links_list
        self.number_of_demands = number_of_demands
        self.demands_list = demands_list
        self.demand_solution = demand_solution

    def print(self):
        print('### INPUT ###')
        print(f'Number of links: {self.number_of_links}')
        print(f'Number of demands: {self.number_of_demands}')

        for idx, link in enumerate(self.links_list):
            link.print()

        for idx, demand in enumerate(self.demands_list):
            demand.print()
