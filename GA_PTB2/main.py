from bitarray import bitarray
import random
from bitarray.util import ba2int, int2ba

a, b, c = 1, -14, 49

class Chromosome:
    def __init__(self, bits, fitness=0):
        self.bits = bits
        self.fitness = fitness

    def crossover(self, other, crossover_point=None):
        if crossover_point is None:
            crossover_point = random.randint(1, len(self.bits) - 1)

        child1_bits = self.bits[:crossover_point] + other.bits[crossover_point:]
        child2_bits = other.bits[:crossover_point] + self.bits[crossover_point:]

        child1 = Chromosome(child1_bits)
        child2 = Chromosome(child2_bits)

        return child1, child2

def integer_to_bit_array(n, length):
    return int2ba(n, length)

def bit_array_to_integer(bit_arr):
    return ba2int(bit_arr)

def create_population(population_size, individual_length=4):
    population = []
    for _ in range(population_size):
        individual = bitarray([random.choice([0, 1]) for _ in range(individual_length)])
        fitness = calculate_fitness(individual, a, b, c)
        chromosome = Chromosome(individual, fitness)
        population.append(chromosome)
    return population

def calculate_fitness(individual, a, b, c):
    x = ba2int(individual)
    return abs(a * x**2 + b * x + c)

def roulette_wheel_selection(population):
    total_fitness = sum(1.0 / (chromosome.fitness + 1) for chromosome in population)
    selection_probs = [
        (1.0 / (chromosome.fitness + 1)) / total_fitness for chromosome in population
    ]

    selected = random.choices(population, weights=selection_probs, k=len(population))
    return selected

def tournament_selection(population, tournament_size=3):
    selected = []
    for _ in range(len(population)):
        tournament = random.sample(population, tournament_size)
        winner = min(tournament, key=lambda x: x.fitness)
        selected.append(winner)
    return selected

def rank_selection(population):
    population = sorted(population, key=lambda x: x.fitness)
    ranks = range(1, len(population) + 1)
    total_rank = sum(ranks)
    selection_probs = [rank / total_rank for rank in ranks]

    selected = random.choices(population, weights=selection_probs, k=len(population))
    return selected

def mutate(individual, mutation_rate=0.01):
    for i in range(len(individual.bits)):
        if random.random() < mutation_rate:
            individual.bits[i] = not individual.bits[i]
    individual.fitness = calculate_fitness(individual.bits, a, b, c)

def evolve_population(population, mutation_rate=0.01):
    new_population = []
    selected_population = tournament_selection(population)
    # Lai ghép và đột biến
    for i in range(0, len(selected_population), 2):
        parent1 = selected_population[i]
        parent2 = (
            selected_population[i + 1]
            if i + 1 < len(selected_population)
            else selected_population[0]
        )
        child1, child2 = parent1.crossover(parent2)

        # Đột biến
        mutate(child1, mutation_rate)
        mutate(child2, mutation_rate)

        new_population.extend([child1, child2])

    # Đảm bảo số lượng cá thể mới bằng số lượng cá thể ban đầu
    if len(new_population) > len(population):
        new_population = new_population[: len(population)]

    return new_population


def main():
    population_size = 5
    individual_length = 4
    generations = 20
    # Tạo quần thể ban đầu
    population = create_population(population_size, individual_length)

    print("Quần thể ban đầu:")
    for individual in population:
        print(
            f"{individual.bits.to01()} => {bit_array_to_integer(individual.bits)}, Fitness: {individual.fitness}"
        )

    for generation in range(generations):
        print(f"\nThế hệ {generation + 1}:")
        population = evolve_population(population)
        for individual in population:
            print(
                f"{individual.bits.to01()} => {bit_array_to_integer(individual.bits)}, Fitness: {individual.fitness}"
            )

            # Dừng nếu tìm thấy nghiệm với fitness bằng 0
            if individual.fitness == 0:
                print(
                    f"\nNghiệm tìm được ở thế hệ {generation + 1}: x = {bit_array_to_integer(individual.bits)}"
                )
                return

    # Nếu không tìm thấy nghiệm sau số thế hệ đã định
    best_solution = min(population, key=lambda x: x.fitness)
    print(
        f"\nKhông tìm thấy nghiệm chính xác sau {generations} thế hệ. Giá trị gần đúng nhất là x = {bit_array_to_integer(best_solution.bits)}, Fitness: {best_solution.fitness}"
    )


if __name__ == "__main__":
    main()