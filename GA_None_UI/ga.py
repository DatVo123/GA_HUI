import random
import time
from bitarray import bitarray
from bitarray.util import ba2int
import psutil

from baseClass import Chromosome, TransactionProcessor, FitnessCalculator

class GeneticAlgorithm:
    def __init__(self, dataset_path, min_utility, population_size, generations, crossover_prob, mutation_prob, output):
        self.dataset_path = dataset_path
        self.population = []
        self.population_size = population_size
        self.generations = generations
        self.min_utility = min_utility
        self.mutation_prob = mutation_prob
        self.crossover_prob = crossover_prob
        self.output = output

        self.hui_sets = set()
        self.biggest_item = 0
        self.avg_len = 0
        self.transactions = []
        self.processor = TransactionProcessor()
        self.existing_chromosomes = set()
        self.total_time = 0

    def load_transactions(self):
        """Load transactions from the dataset and calculate statistics."""
        print("* Loading transactions...")
        start_time = time.time()
        self.transactions = self.processor.load_transactions(self.dataset_path)
        self.biggest_item = self.processor.biggest_item
        self.avg_len = sum(len(tran.tran_bits) for tran in self.transactions) // len(self.transactions)
        total_time = time.time() - start_time
        print(f"* Loading successful: ~ {total_time:.3f} s")
        self.total_time += total_time

    def fitness(self, chromosome_bits):
        """Calculate the fitness of a chromosome."""
        calculator = FitnessCalculator(self.transactions, chromosome_bits)
        return calculator.calculate()

    def chromosome_exists(self, chromosome_bits):
        """Check if a chromosome already exists in the population."""
        int_bit = ba2int(chromosome_bits)
        if int_bit in self.existing_chromosomes:
            return True
        self.existing_chromosomes.add(int_bit)
        return False

    def insert_hui_set(self, chromosome):
        """Insert a high-utility itemset into the set."""
        if chromosome.fitness >= self.min_utility:
            bits_tuple = tuple(chromosome.bits)
            self.hui_sets.add((bits_tuple, chromosome.fitness))

    def generate_initial_population(self):
        """Generate the initial population of chromosomes."""
        print("* Generating initial population...")
        start_time = time.time()
        population = []

        while len(population) < self.population_size:
            chromosome_bits = bitarray(self.biggest_item)
            chromosome_bits.setall(0)
            
            n = random.randint(1, self.avg_len)
            random_positions = random.sample(range(self.biggest_item), n)
            
            for pos in random_positions:
                chromosome_bits[pos] = 1

            chromosome_node = Chromosome(chromosome_bits)
            chromosome_node.fitness = self.fitness(chromosome_node.bits)

            if not self.chromosome_exists(chromosome_node.bits):
                self.existing_chromosomes.add(ba2int(chromosome_node.bits))
                if chromosome_node.fitness >= self.min_utility:
                    self.insert_hui_set(chromosome_node)
                population.append(chromosome_node)

        self.population = sorted(population, key=lambda x: x.fitness, reverse=True)
        total_time = time.time() - start_time
        print(f"* Population generated: ~ {total_time:.3f} s")
        self.total_time += total_time

    def select_parents(self):
        """Select two parents for crossover."""
        length = len(self.population)
        half_length = length // 2
        parent_1 = self.population[random.randint(0, half_length - 1)]
        parent_2 = self.population[random.randint(half_length, length - 1)]
        return parent_1, parent_2

    def crossover(self, parent_1, parent_2):
        """Perform crossover between two parents."""
        s = random.randint(1, self.biggest_item // 2)
        e = random.randint(s + 1, self.biggest_item - 1)
        child_1_bits = parent_1.bits[:s] + parent_2.bits[s:e] + parent_1.bits[e:]
        child_2_bits = parent_2.bits[:s] + parent_1.bits[s:e] + parent_2.bits[e:]
        child_1 = Chromosome(child_1_bits, self.fitness(child_1_bits))
        child_2 = Chromosome(child_2_bits, self.fitness(child_2_bits))
        return child_1, child_2

    def mutate(self, chromosome):
        """Mutate a chromosome."""
        bit_pos = random.randint(0, len(chromosome.bits) - 1)
        chromosome.bits[bit_pos] = not chromosome.bits[bit_pos]
        chromosome.fitness = self.fitness(chromosome.bits)
        return chromosome


    def handle_crossover(self, parent_1, parent_2, new_population):
        """Add crossover offspring to the population."""
        child_1, child_2 = self.crossover(parent_1, parent_2)
        if not self.chromosome_exists(child_1.bits):
            new_population.append(child_1)
            if child_1.fitness >= self.min_utility:
                self.insert_hui_set(child_1)
        if not self.chromosome_exists(child_2.bits):
            new_population.append(child_2)
            if child_2.fitness >= self.min_utility:
                self.insert_hui_set(child_2)

    def handle_mutate(self, new_population):
        """Add mutated chromosome to the population."""
        mutated = self.mutate(random.choice(new_population))
        if not self.chromosome_exists(mutated.bits):
            new_population.append(mutated)
            if mutated.fitness >= self.min_utility:
                self.insert_hui_set(mutated)
    
    def generate_offspring(self, new_population):
        """Generate offspring by crossover and mutation."""
        while len(new_population) < self.population_size:
            parent_1, parent_2 = self.select_parents()
            if random.random() < self.crossover_prob:
                self.handle_crossover(parent_1, parent_2, new_population)
            else:
                new_population.extend([parent_1, parent_2])

            if random.random() < self.mutation_prob:
                self.handle_mutate(new_population)

    def update_population(self, new_population):
        """Update the population with new chromosomes."""
        self.population = sorted(new_population, key=lambda x: x.fitness, reverse=True)

    def evolve_population(self):
            """Evolve the population over several generations."""
            for generation in range(self.generations):
                start_time = time.time()
                new_population = self.population[:self.population_size // 2]
                print(f"+ Generation {generation + 1}:", end=" ")
                self.generate_offspring(new_population)
                total_time = time.time() - start_time
                print(f"~ {total_time:.3f} s")
                self.total_time += total_time
            self.update_population(new_population)

    def report_performance(self):
        """Report performance metrics."""
        memory_info = psutil.Process().memory_info()
        print(f"> High-utility itemsets found: {len(self.hui_sets)}")
        print(f"> Total time: ~ {self.total_time:.3f} s")
        print(f"> Max memory: ~ {memory_info.rss / 1024 / 1024:.3f} MB")
        self.total_memory = f"Max memory: ~ {memory_info.rss / 1024 / 1024:.3f} MB"

    def save_files(self):
        """Save results to an output file."""
        with open(self.output, "w") as f:
            f.write(f"Total High-utility itemsets found: {len(self.hui_sets)}\n")
            f.write(f'Total time: {self.total_time:.3f} s\n')
            f.write(self.total_memory + '\n')
            f.write("-------------------\n")
            for bits, fitness in self.hui_sets:
                if fitness >= self.min_utility:
                    items = [i + 1 for i in range(len(bits)) if bits[i]]
                    items_str = " ".join(str(item) for item in items)
                    f.write(f"{items_str} #UTIL: {fitness}\n")

    def execute(self):
        """Execute the genetic algorithm."""
        self.load_transactions()
        self.generate_initial_population()
        self.evolve_population()
        self.report_performance()
        self.save_files()