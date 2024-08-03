import random
import time
from bitarray import bitarray
from bitarray.util import ba2int

import psutil

from baseClass import Chromosome, TransactionProcessor, FitnessCalculator

from PyQt6.QtCore import QObject, pyqtSignal

class GeneticAlgorithm(QObject):
    progress_update = pyqtSignal(str)

    def __init__(self, dataset_path, min_utility, population_size, generations, crossover_prob, mutation_prob, output="output.txt"):
        super().__init__()
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

        self.cancel_requested = False

    def load_transactions(self):
        self.transactions = self.processor.load_transactions(self.dataset_path)
        self.biggest_item = self.processor.biggest_item
        self.avg_len = sum(len(tran.tran_bits) for tran in self.transactions) // len(self.transactions)

    def fitness(self, chromosome_bits):
        calculator = FitnessCalculator(self.transactions, chromosome_bits)
        return calculator.calculate()

    def chromosome_exists(self, chromosome_bits):
        int_bit = ba2int(chromosome_bits)
        if int_bit in self.existing_chromosomes:
            return True
        self.existing_chromosomes.add(int_bit)
        return False

    def insert_hui_set(self, chromosome):
        if chromosome.fitness >= self.min_utility:
            bits_tuple = tuple(chromosome.bits)
            self.hui_sets.add((bits_tuple, chromosome.fitness))

    def generate_initial_population(self):
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

            int_bit = ba2int(chromosome_node.bits)
            self.existing_chromosomes.add(int_bit)

            if chromosome_node.fitness >= self.min_utility:
                self.insert_hui_set(chromosome_node)

            population.append(chromosome_node)

        sorted_population = sorted(population, key=lambda x: x.fitness, reverse=True)
        self.population = sorted_population

    def select_parents(self):
        length = len(self.population)
        half_length = length // 2
        parent_1 = self.population[random.randint(0, half_length - 1)]
        parent_2 = self.population[random.randint(half_length, length - 1)]
        return parent_1, parent_2

    def crossover(self, parent_1, parent_2):
        s = random.randint(1, self.biggest_item // 2)
        e = random.randint(s + 1, self.biggest_item - 1)
        child_1_bits = parent_1.bits[:s] + parent_2.bits[s:e] + parent_1.bits[e:]
        child_2_bits = parent_2.bits[:s] + parent_1.bits[s:e] + parent_2.bits[e:]
        return Chromosome(child_1_bits, self.fitness(child_1_bits)), Chromosome(child_2_bits, self.fitness(child_2_bits))

    def mutate(self, chromosome):
        bit_pos = random.randint(0, len(chromosome.bits) - 1)
        chromosome.bits[bit_pos] = not chromosome.bits[bit_pos]
        chromosome.fitness = self.fitness(chromosome.bits)
        return chromosome

    def execute(self):
        start_time = time.time()
        self.progress_update.emit("Reading transaction...")
        self.load_transactions()
        self.progress_update.emit(f"Reading completed in {(time.time() - start_time):.3f}s")
        time.sleep(1)
        self.generate_initial_population()
        self.progress_update.emit("Initial population generated.")
        time.sleep(1)
        if self.cancel_requested:
            self.progress_update.emit(f"\n-------------------\nTotal time: ~ {time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))} s")
            self.progress_update.emit(f"Memory: ~ {psutil.Process().memory_info().rss / 1024 / 1024:.3f} MB")
            self.progress_update.emit("Algorithm execution has been canceled.")
            self.cancel_requested = False
            return
        else:
            for generation in range(self.generations):
                if self.cancel_requested:
                    self.progress_update.emit(f"\n-------------------\nTotal time: ~ {time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))} s")
                    self.progress_update.emit(f"Memory: ~ {psutil.Process().memory_info().rss / 1024 / 1024:.3f} MB")
                    self.progress_update.emit("Algorithm execution has been canceled.")
                    return
                new_population = self.population[:self.population_size // 2]
                generation_start_time = time.time()

                while len(new_population) < self.population_size:
                    if self.cancel_requested:
                        self.progress_update.emit(f"\n-------------------\nTotal time: ~ {time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))} s")
                        self.progress_update.emit(f"Memory: ~ {psutil.Process().memory_info().rss / 1024 / 1024:.3f} MB")
                        self.progress_update.emit("Algorithm execution has been canceled.")
                        self.cancel_requested = False
                        return
                    parent_1, parent_2 = self.select_parents()
                    if random.random() < self.crossover_prob:
                        child_1, child_2 = self.crossover(parent_1, parent_2)
                        if not self.chromosome_exists(child_1.bits):
                            new_population.append(child_1)
                        if not self.chromosome_exists(child_2.bits):
                            new_population.append(child_2)
                        if child_1.fitness >= self.min_utility:
                            self.insert_hui_set(child_1)
                        if child_2.fitness >= self.min_utility:
                            self.insert_hui_set(child_2)
                    else:
                        new_population.extend([parent_1, parent_2])

                    if random.random() < self.mutation_prob:
                        mutated = self.mutate(random.choice(new_population))
                        if not self.chromosome_exists(mutated.bits):
                            new_population.append(mutated)
                        if mutated.fitness >= self.min_utility:
                            self.insert_hui_set(mutated)

                    # Sort new_population by fitness
                    new_population = sorted(new_population, key=lambda x: x.fitness, reverse=True)

                self.population = new_population
                generation_time = time.time() - generation_start_time
                self.progress_update.emit(f"Generation {generation + 1} completed in ~ {generation_time:.3f} s.")

            self.total_time = f"\n-------------------\nTotal time: ~ {time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))}s\n"
            self.total_memory = f"Memory: ~ {psutil.Process().memory_info().rss / 1024 / 1024:.3f} MB"
            self.cancel_requested = False
            self.progress_update.emit("Algorithm execution completed.")