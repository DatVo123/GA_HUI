from ga import GeneticAlgorithm

if __name__ == '__main__':
    dataset_path = 'Dataset/accidents.txt'
    min_utility = 30
    population_size = 50
    generations = 100
    crossover_prob = 0.8
    mutation_prob = 0.1

    ga = GeneticAlgorithm(dataset_path, min_utility, population_size, generations, crossover_prob, mutation_prob)
    ga.execute()