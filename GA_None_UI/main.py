from ga import GeneticAlgorithm

if __name__ == '__main__':
    dataset_path = 'Dataset/test.txt'
    min_utility = 15
    population_size = 5
    generations = 5
    crossover_prob = 0.8
    mutation_prob = 0.1

    ga = GeneticAlgorithm(dataset_path, min_utility, population_size, generations, crossover_prob, mutation_prob)
    ga.execute()