import sys
import os
import time
from random import randint


easy_path = os.path.join("test_data", "low_dimensional")
hard_path = os.path.join("test_data", "large_scale")
easy_path_full = os.path.join("test_data", "tmp_low_dimensional")


def get_test_data(path):
    data = []
    for name in os.listdir(path):
        with open(os.path.join(path, name), "r") as file:
            example = {"weights": [], "values": []}
            data_params = file.readline().split(" ")
            example["capacity"] = int(data_params[1])
            example["data_set"] = name
            example["size"] = int(data_params[0])
            for line in file:
                pairs = line.split(" ")
                example["weights"].append(int(pairs[1]))
                example["values"].append(int(pairs[0]))

        with open(os.path.join(path + "_optimum", name), "r") as file:
            example["optimum"] = int(file.read().strip())

        data.append(example)

    return data

def generate_test_data(size, ratio):
    """Generates test data  where 
        size = number of items
        ratio = backpack capacity / average item weight (uniform dist.)
        or average number of items fitting in backpack"""
    max_weight = 100
    example = {"capacity": int(max_weight / 2 * ratio)}
    example["weights"] = [randint(1, max_weight) for _ in range(size)]
    example["values"] = [randint(1, 100) for _ in range(size)]
    example["optimum"] = None
    return example


def test_alg(func, data, rounds):
    """ Tests given function with params: (capacity, weights, values) which returns optimum """
    for example in data:
        avg_time = []
        avg_result = []
        for i in range(0, rounds):
            start_time = time.clock()
            avg_result.append(func(example["capacity"], example["weights"], example["values"]))
            avg_time.append(time.clock() - start_time)
        print("Result for dataset:\t%s , size:\t%s" % (example["data_set"], example["size"]))
        print("Average execution time:\t", '{:.3}'.format(sum(avg_time)/rounds), " seconds")
        avg_result_value = sum(avg_result)/rounds
        print("accuracy:\t", '{:.1%}'.format(avg_result_value/example["optimum"]), "\t optimum: \t%d\t average result: \t%d" % (example["optimum"], avg_result_value))
        print("\n")


W = 50
w = [10, 20, 30]
c = [60, 100, 120]
values_a = [135, 139, 149, 150, 156, 163, 173, 184, 192, 201, 210, 214, 221, 229, 240]
sizes_a = [70, 73, 77, 80, 82, 87, 90, 94, 98, 106, 110, 113, 115, 118, 120]
capacity_a = 750