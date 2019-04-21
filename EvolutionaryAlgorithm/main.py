from parser import read_file
from writer import write_file
from brute_solver import brute_solve
from evolutionary_solver import evolutionary_solve
from constants import USAGE


def print_usage():
    print(USAGE)


def main():
    """ Main program """
    print_usage()

    network_4 = read_file('data/net4.txt')
    network_4.print()

    # Find solutions.
    network = brute_solve(network_4)
    write_file('output/net4_brute_solution.txt', network)
    network = evolutionary_solve(network_4)
    write_file('output/net4_evolutionary_solution.txt', network)
    return 0


if __name__ == "__main__":
    main()