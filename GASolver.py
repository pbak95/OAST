from random import randint, choice
from itertools import chain
import math

DEBUG = False

class Backpack:
	def __init__(self, weights, values, capacity):
		self.weights = weights
		self.values = values
		self.capacity = capacity
		self.items_number = len(weights)

	def get_weight(self, item_array):
		weights = [x for x, y  in zip(self.weights, item_array) if y == 1]
		return sum(weights)
	def get_value(self, item_array):
		values = [x for x, y  in zip(self.values, item_array) if y == 1]
		return sum(values)
	def get_fitness(self, item_array):
		values = [x for x, y  in zip(self.values, item_array) if y == 1]
		weights = [x for x, y  in zip(self.weights, item_array) if y == 1]
		overload = sum(weights) - self.capacity
		is_over = int(overload > 0)
		return int(sum(values) - is_over * (overload**2 / 2 + self.capacity / 2 ))

def selection(population, fitnesses):
	fitness_sum = sum([max(x, 0) for x in fitnesses])
	a = randint(1, max(fitness_sum, 2))
	b = randint(1, max(fitness_sum, 2))
	selected_a = None
	selected_b = None

	for f in fitnesses:
		fitness_sum -= f
		if (fitness_sum < a): selected_a = population[fitnesses.index(f)]
		if (fitness_sum < b): selected_b = population[fitnesses.index(f)]
		if (fitness_sum <= 0 or(selected_a != None and selected_b != None)): break

	return (selected_a, selected_b)
def single_init(items_number):
    index = randint(0, items_number - 1)
    return [1 if i ==  index else 0 for i in range(items_number)] 

def crossover(x, y):
	size = len(x)
	locus = randint(0, size-1)
	child_a = x[:locus] + y[locus:]
	child_b = y[:locus] + x[locus:]
	return child_a, child_b

def flip_mutation(x, prob):
	mutation_indices = [randint(0, int(1/prob)) == 0  for i in range(len(x))]
	return [int(bool(a) ^ bool(b)) for a, b in zip(x, mutation_indices)]

def exchange_mutation(x, prob):
	"""With probability prob takes every 1 in x and moves it to random place (either with 0 or 1) """
	for i in range(len(x)-1):
		if(x[i]):
			if(randint(0, int(1/prob)) == 0):
				x[randint(0, len(x)-1)] = 1
				x[i] = 0
	return x 

def ga_solver(capacity, sizes, values):
	b = Backpack(sizes, values, capacity)

	population_size = 15
	items_number = b.items_number

	population = [single_init(items_number) for _ in range(population_size)]
	fitnesses = [b.get_fitness(x) for x in population]
	best_of_iter = []
	i = 0
	while True:
		if DEBUG:
			print(i)
		#sort
		fitnesses, population = zip(*sorted(zip(fitnesses, population), reverse = True))
		fitnesses = list(fitnesses)
		population = list(population)
		if DEBUG:
			print("fitnesses", fitnesses)
			#print("population", population)
			# for x in population:
			# 	print([index for index in range(len(x)) if x[index]])

		#selection of pairs
		pairs = [(selection(population, fitnesses)) for x in range(math.floor(population_size/2)-1)]
		if DEBUG:
			print("pairs", pairs)

		#crossover
		new_population = [crossover(x, y) for (x, y) in pairs] #crossover returns tuples that must be unpacked
		new_population = list(chain.from_iterable(new_population))
		if DEBUG:
			print("crossed", new_population)

		#mutation
		new_population = list(map(lambda x: exchange_mutation(x, 0.1), new_population))
		new_population = list(map(lambda x: flip_mutation(x, 0.01), new_population))

		if DEBUG:
			print("mutated", new_population)

		#update population
		population = new_population + population[0:3]
		fitnesses = [b.get_fitness(x) for x in population]
		best_value = b.get_value(population[fitnesses.index(max(fitnesses))])
		best_of_iter.append(best_value)

		if DEBUG:
			print("best: ", best_value)
		i += 1
		#stop criterium
		
		if(i>200):
			if (best_of_iter[i-60] == best_of_iter[i - 1]): break

	return best_of_iter[-1]