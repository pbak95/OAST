from GASolver.dynamicSolver import dynamic_alg
from GASolver.tester import get_test_data, easy_path, test_alg
from GASolver.GASolver import ga_solver

data = get_test_data(easy_path)

print("[dynamic_alg]:")
test_alg(dynamic_alg, data, 3)

print("[ga_solver]")
test_alg(ga_solver, data, 3)

# example = generate_test_data(50, 10)
# example["optimum"] = dynamic_alg(example["capacity"], example["weights"], example["values"])
# test_alg(ga_solver, [example])
