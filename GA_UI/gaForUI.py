import os
import random
import time
from bitarray import bitarray
import psutil

from baseClass import Individual, TransactionProcessor, FitnessCalculator
from PyQt6.QtCore import QObject, pyqtSignal 
class GeneticAlgorithm(QObject):
    progress_update = pyqtSignal(str)

    def __init__(self, dataset_path, min_utility, generations, population_size, crossover_prob, mutation_prob):
        super().__init__()
        self.dataset_path = dataset_path
        self.population = []
        self.population_size = population_size
        self.generations = generations
        self.min_utility = min_utility
        self.mutation_prob = mutation_prob
        self.crossover_prob = crossover_prob

        self.hui_sets = set()
        self.biggest_item = 0
        self.avg_len = 0
        self.transactions = []
        self.processor = TransactionProcessor()
        self.total_time = 0
        self.cancel_requested = False
    def load_transactions(self):
        """Load transactions from the dataset."""
        self.progress_update.emit("* Loading Transactions...")
        start_time = time.time()
        try:
            if self.cancel_requested:
                self.cancel_progress()
                return
            self.transactions = self.processor.load_transactions(self.dataset_path)
            self.biggest_item = self.processor.biggest_item
            self.avg_len = sum(len(tran.tran_bits) for tran in self.transactions) // len(self.transactions)
            total_time = time.time() - start_time
            self.progress_update.emit(f"Loaded Successful in: ~ {total_time:.3f} s")
            self.total_time += total_time
        except Exception as e:
            self.progress_update.emit(f"Error occurred while loading transactions: {e}")

    def fitness(self, Individual_bits):
        """Calculate the fitness of an individual."""
        try:
            calculator = FitnessCalculator(self.transactions, Individual_bits)
            return calculator.calculate()
        except Exception as e:
            self.progress_update.emit(f"Error occurred while calculating fitness: {e}")
            return 0

    def individual_exists(self, individual_bits):
        """Check if an individual already exists in the population."""
        for Individual in self.population:
            if Individual.bits == individual_bits:
                return True
        return False

    def insert_hui_set(self, individual):
        """Insert a high-utility itemset into the set."""
        if individual.fitness >= self.min_utility:
            bits_tuple = tuple(individual.bits)
            self.hui_sets.add((bits_tuple,individual.fitness))

    def generate_initial_population(self):
        """Generate the initial population of Individuals."""
        self.progress_update.emit("* Generating Initial Population...")
        start_time = time.time()

        try:
            while len(self.population) < self.population_size:
                if self.cancel_requested:
                    return
                
                Individual_bits = bitarray(self.biggest_item)
                Individual_bits.setall(0)

                n = random.randint(1, self.avg_len)
                random_positions = random.sample(range(self.biggest_item), n)
                for pos in random_positions:
                    Individual_bits[pos] = 1

                individual = Individual(Individual_bits)
                individual.fitness = self.fitness(individual.bits)
                if not self.individual_exists(individual.bits):
                    if individual.fitness is not None and individual.fitness >= self.min_utility:
                        self.insert_hui_set(individual)
                    self.population.append(individual)

            self.population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        except Exception as e:
            self.progress_update.emit(f"Error occurred during initial population generation: {e}")

        total_time = time.time() - start_time
        self.progress_update.emit(f"Generated Population in ~ {total_time:.3f} s")
        self.total_time += total_time

    def tournament_selection(self):
        """Select a subset of individuals and choose the best one from the subset."""
        k = random.randint(1,len(self.population))
        tournament = random.sample(self.population, k)
        return max(tournament, key=lambda x: x.fitness)

    def roulette_wheel_selection(self):
        """Select an individual based on the fitness proportionate to the total fitness of the population."""
        total_fitness = sum(individual.fitness for individual in self.population)
        if total_fitness == 0:
            return random.choice(self.population)
        
        selection_probabilities = [individual.fitness / total_fitness for individual in self.population]
        selected_index = random.choices(range(len(self.population)), weights=selection_probabilities, k=1)[0]
        return self.population[selected_index]

    def rank_selection(self):
        """Select an individual based on its rank in the sorted population."""
        sorted_population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        num_individuals = len(sorted_population)
        total_ranks = sum(range(1, num_individuals + 1))
        rank_probabilities = [(num_individuals - rank + 1) / total_ranks for rank in range(1, num_individuals + 1)]
        selected_index = random.choices(range(num_individuals), weights=rank_probabilities, k=1)[0]
        return sorted_population[selected_index]

    def single_point_crossover(self, parent_1, parent_2):
        """Perform single_point crossover between two parents."""
        s = random.randint(1, self.biggest_item // 2)
        e = random.randint(s + 1, self.biggest_item - 1)
        child_1_bits = parent_1.bits[:s] + parent_2.bits[s:e] + parent_1.bits[e:]
        child_2_bits = parent_2.bits[:s] + parent_1.bits[s:e] + parent_2.bits[e:]
        child_1 = Individual(child_1_bits, self.fitness(child_1_bits))
        child_2 = Individual(child_2_bits, self.fitness(child_2_bits))
        return child_1, child_2

    def multi_point_crossover(self, parent_1, parent_2):
        """Perform multi-point crossover between two parents with random."""
        points = sorted(random.sample(range(self.biggest_item), self.biggest_item//2))
        child_1_bits = parent_1.bits[:points[0]]
        child_2_bits = parent_2.bits[:points[0]]
        
        for i in range(len(points) - 1):
            if i % 2 == 0:
                child_1_bits += parent_2.bits[points[i]:points[i + 1]]
                child_2_bits += parent_1.bits[points[i]:points[i + 1]]
            else:
                child_1_bits += parent_1.bits[points[i]:points[i + 1]]
                child_2_bits += parent_2.bits[points[i]:points[i + 1]]

        if len(points) % 2 == 0:
            child_1_bits += parent_2.bits[points[-1]:]
            child_2_bits += parent_1.bits[points[-1]:]
        else:
            child_1_bits += parent_1.bits[points[-1]:]
            child_2_bits += parent_2.bits[points[-1]:]
        
        child_1 = Individual(child_1_bits, self.fitness(child_1_bits))
        child_2 = Individual(child_2_bits, self.fitness(child_2_bits))
        
        return child_1, child_2

    def uniform_crossover(self, parent_1, parent_2):
        """Perform uniform crossover between two parents."""
        child_1_bits = bitarray(self.biggest_item)
        child_2_bits = bitarray(self.biggest_item)
        
        for i in range(self.biggest_item):
            if random.random() < 0.5:
                child_1_bits[i] = parent_1.bits[i]
                child_2_bits[i] = parent_2.bits[i]
            else:
                child_1_bits[i] = parent_2.bits[i]
                child_2_bits[i] = parent_1.bits[i]
        
        child_1 = Individual(child_1_bits, self.fitness(child_1_bits))
        child_2 = Individual(child_2_bits, self.fitness(child_2_bits))
        return child_1, child_2

    def crossover(self, parent_1, parent_2):
        """Perform crossover on a random method."""
        crossover_method = random.choice(
            [self.single_point_crossover(parent_1,parent_2),
            self.multi_point_crossover(parent_1,parent_2),
            self.uniform_crossover(parent_1,parent_2)])
        return crossover_method

    def mutate(self, individual):
        """Mutate an individual."""
        bit_pos = random.randint(0, len(individual.bits) - 1)
        individual.bits[bit_pos] = not individual.bits[bit_pos]
        individual.fitness = self.fitness(individual.bits)
        return individual

    def handle_crossover(self, parent_1, parent_2, new_population):
        """Add crossover offspring to the population"""
        try:
            child_1, child_2 = self.crossover(parent_1, parent_2)
            
            if not self.individual_exists(child_1.bits):
                new_population.append(child_1)
                if child_1.fitness >= self.min_utility:
                    self.insert_hui_set(child_1)
            
            if not self.individual_exists(child_2.bits):
                new_population.append(child_2)
                if child_2.fitness >= self.min_utility:
                    self.insert_hui_set(child_2)
        except Exception as e:
            self.progress_update.emit(f"An error occurred during crossover: {e}")
            return

    def handle_mutate(self, new_population):
        """Add mutated offspring to the population"""
        try:
            num_mutations = len(new_population)//8
            for _ in range(num_mutations):
                mutated = self.mutate(random.choice(new_population))
                if not self.individual_exists(mutated.bits):
                    new_population.append(mutated)
                    if mutated.fitness >= self.min_utility:
                        self.insert_hui_set(mutated)
        except Exception as e:
            self.progress_update.emit(f"An error occurred during mutation: {e}")
            return

    def select_parents(self):
        """Select two distinct parents from the population."""
        parent_1 = random.choice([self.tournament_selection(), self.roulette_wheel_selection(), self.rank_selection()])
        parent_2 = parent_1
        while parent_2 == parent_1:
            parent_2 = random.choice([self.tournament_selection(), self.roulette_wheel_selection(), self.rank_selection()])
        return parent_1, parent_2

    def handle_offspring(self, parent_1, parent_2, new_population):
        """Handle crossover and mutation of offspring."""
        if random.random() < self.crossover_prob:
            self.handle_crossover(parent_1, parent_2, new_population)
        if random.random() < self.mutation_prob:
            self.handle_mutate(new_population)

    def generate_offspring(self, new_population):
        """Generate offspring by crossover and mutation."""
        while len(new_population) < self.population_size:
            if self.cancel_requested:
                return
            parent_1, parent_2 = self.select_parents()
            self.handle_offspring(parent_1, parent_2, new_population)

    def update_population(self, new_population):
        """Update the population with new Individuals."""
        new_population_sorted = sorted(new_population, key=lambda x: x.fitness, reverse=True)
        if len(new_population) > self.population_size:
            self.population = new_population_sorted[:self.population_size]

    def evolve_population(self):
        """Evolve the population over several generations"""
        try:
            for generation in range(self.generations):
                start_time = time.time()
                new_population = self.population[:self.population_size//2]
                self.generate_offspring(new_population)
                total_time = time.time() - start_time
                self.total_time += total_time
                self.progress_update.emit(f"Evolving Generation {generation + 1} in ~ {total_time:.3f} s")
                self.update_population(new_population)
                if self.cancel_requested:
                    return

        except Exception as e:
            self.progress_update.emit(f"An error occurred during population evolution: {e}")
            return

    def report_performance(self):
        """Report performance metrics."""
        self.total_memory = psutil.Process().memory_info().rss
        self.progress_update.emit(f"\nReport performance for database: {os.path.splitext(os.path.basename(self.dataset_path))[0]}")
        self.progress_update.emit(f"Total time: ~ {self.total_time:.3f} s")
        self.progress_update.emit(f"Total memory used: ~ {self.total_memory / 1024 / 1024:.3f} MB")

    def write_header(self, file):
        """Write header information to the file."""
        file.write(f'Genetic Algorithm Result For Database: {os.path.splitext(os.path.basename(self.dataset_path))[0]} \n')
        file.write(f'Total time: {self.total_time:.3f} s\n')
        file.write(f'Total memory used: ~ {self.total_memory / 1024 / 1024:.3f} MB\n')
        file.write(f"Total High-utility item-sets found: {len(self.hui_sets)}\n\n")

    def write_hui_sets(self, file):
        """Write high-utility itemsets to the file."""
        for bits, fitness in self.hui_sets:
            if fitness >= self.min_utility:
                items = [i + 1 for i in range(len(bits)) if bits[i]]
                items_str = " ".join(str(item) for item in items)
                file.write(f"{items_str} #UTIL: {fitness}\n")

    def save_files(self, output):
        """Save results to an output file."""
        with open(output, "w") as file:
            self.write_header(file)
            self.write_hui_sets(file)

    def execute(self):
        """Execute the genetic algorithm."""
        try:
            self.load_transactions()
            self.generate_initial_population()
            self.evolve_population()
            self.cancel_progress()
            self.report_performance()
        except Exception as e:
            self.progress_update.emit(f"An error occurred during the execution of the genetic algorithm: {e}")
            return
    def cancel_progress(self):
        if self.cancel_requested:
            self.progress_update.emit("\nAlgorithm execution has been canceled.")
