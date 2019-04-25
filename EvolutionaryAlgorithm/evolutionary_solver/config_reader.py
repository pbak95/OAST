class Config(object):
    def __init__(self, seed, population_size, mutation_probability, stop, stop_arg):
        self.seed = seed
        self.population_size = population_size
        self.mutation_probability = mutation_probability
        self.stop = stop
        self.stop_arg = stop_arg


def get_config() -> Config:
    # default config values if not set in settings file
    seed = None
    population_size = 10
    mutation_probability = 0.01
    stop = 'best_iter'
    stop_arg = 30
    with open('evolutionary_solver/settings', 'r') as file:
        for current_line in file:
            if not(current_line.startswith("#")):
                if current_line.startswith("seed"):
                    seed = int(current_line.split()[1])
                elif current_line.startswith("population_size"):
                    population_size = int(current_line.split()[1])
                elif current_line.startswith("mutation_probability"):
                    mutation_probability = float(current_line.split()[1])
                elif current_line.startswith("stop"):
                    stop = current_line.split()[1]
                    stop_arg = int(current_line.split()[2])

    return Config(seed, population_size, mutation_probability, stop, stop_arg)


