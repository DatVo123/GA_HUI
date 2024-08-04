from bitarray import bitarray
from bitarray.util import int2ba, ba2int
import random

class Chromosome:
    def __init__(self, bits, a, b, c, fitness=0):
        self.bits = bits
        self.a = a
        self.b = b
        self.c = c
        self.fitness = fitness

    def crossover(self, other, crossover_point=None):
        if crossover_point is None:
            crossover_point = random.randint(1, len(self.bits) - 1)

        child1_bits = self.bits[:crossover_point] + other.bits[crossover_point:]
        child2_bits = other.bits[:crossover_point] + self.bits[crossover_point:]

        return Chromosome(child1_bits, self.a, self.b, self.c), Chromosome(child2_bits, self.a, self.b, self.c)

    def mutate(self, mutation_rate):
        for i in range(len(self.bits)):
            if random.random() < mutation_rate:
                self.bits[i] = not self.bits[i]
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        x = ba2int(self.bits)
        return abs(self.a * x**2 + self.b * x + self.c)

class GeneticAlgorithm:
    def __init__(self, population_size, individual_length, a, b, c, crossover_rate, mutation_rate, tournament_size=3):
        self.population_size = population_size
        self.individual_length = individual_length
        self.a = a
        self.b = b
        self.c = c
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.population = self.create_population()

    def create_population(self):
        population = []
        for _ in range(self.population_size):
            individual = bitarray([random.choice([0, 1]) for _ in range(self.individual_length)])
            chromosome = Chromosome(individual, self.a, self.b, self.c)
            chromosome.fitness = chromosome.calculate_fitness()
            population.append(chromosome)
        return population

    def roulette_wheel_selection(self):
        total_fitness = sum(1.0 / (chromosome.fitness + 1) for chromosome in self.population)
        selection_probs = [
            (1.0 / (chromosome.fitness + 1)) / total_fitness for chromosome in self.population
        ]
        return random.choices(self.population, weights=selection_probs, k=len(self.population))

    def tournament_selection(self):
        selected = []
        for _ in range(len(self.population)):
            tournament = random.sample(self.population, self.tournament_size)
            winner = min(tournament, key=lambda x: x.fitness)
            selected.append(winner)
        return selected

    def rank_selection(self):
        sorted_population = sorted(self.population, key=lambda x: x.fitness)
        ranks = range(1, len(sorted_population) + 1)
        total_rank = sum(ranks)
        selection_probs = [rank / total_rank for rank in ranks]
        return random.choices(sorted_population, weights=selection_probs, k=len(self.population))

    def evolve_population(self):
        new_population = []
        selected_population = self.tournament_selection()

        for i in range(0, len(selected_population), 2):
            parent1 = selected_population[i]
            parent2 = (
                selected_population[i + 1]
                if i + 1 < len(selected_population)
                else selected_population[0]
            )
            
            if random.random() < self.crossover_rate:
                child1, child2 = parent1.crossover(parent2)
            else:
                child1, child2 = parent1, parent2

            child1.mutate(self.mutation_rate)
            child2.mutate(self.mutation_rate)

            new_population.extend([child1, child2])

        if len(new_population) > len(self.population):
            new_population = new_population[: len(self.population)]

        self.population = new_population

    def run(self, generations):
        results = []

        for generation in range(generations):
            self.evolve_population()

            generation_results = [
                f"{individual.bits.to01()} => {ba2int(individual.bits)}, Fitness: {individual.fitness}"
                for individual in self.population
            ]
            results.append(f"Generation {generation + 1}:\n" + "\n".join(generation_results))

            if any(individual.fitness == 0 for individual in self.population):
                break

        best_solution = min(self.population, key=lambda x: x.fitness)
        if best_solution.fitness == 0:
            results.append(f"\nExact solution found: x = {ba2int(best_solution.bits)}, Fitness: {best_solution.fitness}")
        else:
            results.append(f"\nNo exact solution found after {generations} generations. Closest solution: x = {ba2int(best_solution.bits)}, Fitness: {best_solution.fitness}")

        return "\n".join(results)
