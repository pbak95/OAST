#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from brute_solver import brute_solve
from constants import USAGE
from evolutionary_solver import evolutionary_solve
from file_parser import read_file
from file_writer import write_file


def print_usage():
    print(USAGE)


def main():
    """ Main program """
    print_usage()

    network_4 = read_file('data/net12_1.txt')
    network_4.print()

    # Find solutions.
    # network = brute_solve(network_4)
    # network.print()
    # write_file('output/net4_brute_solution.txt', network)

    network = evolutionary_solve(network_4)
    write_file('output/net12_1_best_select_solution_init_2.txt', network)


if __name__ == "__main__":
    main()
