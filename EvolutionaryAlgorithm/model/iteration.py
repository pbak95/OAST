import sys

from .possibilities import Possibilities


class Iteration(object):

    def __init__(self, possibilities: Possibilities):
        self.possibilities = possibilities
        self.values = []
        self.state = [0] * self.possibilities.number_of_demands
        for i in range(0, self.possibilities.number_of_demands):
            self.values.append([0] * self.possibilities.longest_route)

    def next_iteration(self, modules_used: str):
        for i in reversed(range(0, self.possibilities.number_of_demands)):
            # Very important '- 1' here
            if self.state[i] < len(self.possibilities[i]) - 1:
                self.state[i] = self.state[i] + 1
                self.set_values()
                return True
            elif self.state[i - 1] < len(self.possibilities[i - 1]) - 1:
                self.state[i - 1] = self.state[i - 1] + 1
                self.state[i:] = [0] * (self.possibilities.number_of_demands - i)
                if i == 1:
                    self.update_progress(self.state[0] / len(self.possibilities[0]), modules_used)
                self.set_values()
                return True
        return False

    def set_values(self):
        for i in range(0, self.possibilities.number_of_demands):
            self.values[i] = self.possibilities[i][self.state[i]]

    # Displays or updates a console progress bar
    def update_progress(self, progress, modules: str):
        bar_length = 100
        status = ""
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
            status = "error: progress var must be float\r\n"
        if progress < 0:
            progress = 0
            status = "Halt...\r\n"
        if progress >= 1:
            progress = 1
            status = "Done...\r\n"
        block = int(round(bar_length * progress))
        text = "\rModules used: [{3}].. Percent: [{0}] {1}% {2}".format("#" * block + "-" * (bar_length - block),
                                                                        progress * 100, status, modules)
        sys.stdout.write(text)
        sys.stdout.flush()
