from ga import GeneticAlgorithm

if __name__ == '__main__':
    dataset_path = 'Dataset/chicago.txt'
    generations = 25
    population_size = 30
    crossover_prob = 0.5
    mutation_prob = 0.1
    min_utility = 10
    

    ga = GeneticAlgorithm(dataset_path, min_utility, population_size, generations, crossover_prob, mutation_prob)
    ga.execute()