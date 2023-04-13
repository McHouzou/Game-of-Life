"""
Script to evolve certain initial grid configuration, given fitness function.
In essence, it is a Genetic Algorithm Implementation for discovering solutions
(initial configurations) that have certain characteristics in the Game of Life.
"""

import numpy as np
import copy
from Game_of_life import Game_of_life
rng = np.random.default_rng()


GEN = 50        # Number of generations
POP_SIZE = 50   # Population Size
MR = 0.2        # Muation rate
CR = 0.3        # Crossover rate
Elitism = 0.2   # Implement Elitim? (keep a percentage of the fittest individuals unaltered to next generation)
SIZE = 5        # Size of solution grid
Dt = 40         # Number of timesteps to run for each fitness evaluation
N = 25          # Size of y_dimension of whole grid
M = 25          # Size of x_dimension of whole grid


def get_individual_fitness(init_array):
    """
    Fitness function for the individual solution. To be defined depending on what the user wants to achieve.
    e.g. define fitness function as the ratio between the final and initial numbers of alive cells
    after Dt iterations.
    """
    init_array = init_array.reshape((SIZE,SIZE))
    G = Game_of_life(N, M, init_array)

    active_0 = G.count_active()  
    G.run_timesteps(Dt)

    """
    #Or define fitness as the average x velocity of the centre of mass of the whole system
    CM0 = G.current_com()
    G.run_timesteps(Dt)
    CM1 = G.current_com()
    return abs((CM1 - CM0)/Dt)
    """
    return G.count_active()/active_0



def run_evolution():
    population = np.random.randint(2, size=(POP_SIZE, SIZE**2))
    fitnesses = np.zeros(POP_SIZE)

    for g in range(GEN):
        print(f"Generation = {g}")

        #Get fitness for each individual (solution)
        for i in range(population.shape[0]):
            fitnesses[i] = get_individual_fitness(population[i])

        #Sort in ascending order of fitness
        sorted_inds = fitnesses.argsort()
        fitnesses = fitnesses[sorted_inds];   print(fitnesses)
        population = population[sorted_inds]
        fitnesses = fitnesses/np.sum(fitnesses) #normalize fitnes values (so that they add up to 1)

        #Implement elitism
        if (int(Elitism*POP_SIZE) >= 2):
            new_population = copy.deepcopy(population[-int(Elitism*POP_SIZE):])
            n_children = int(Elitism*POP_SIZE)
        else:
            raise TypeError("You need an elitist percentage that is large enough to produce an even number of individuals (not zero)")

        #For the rest of the children population, proceed with crossover
        while n_children < POP_SIZE:
            parents = rng.choice(population, 2, p = fitnesses, replace = False)
            if np.random.random() < CR: #Each pair of parents is crossed over with propability CR.
                split_at = np.random.randint(0, SIZE**2) #Choose position along genetic code to crossover the two solutions.
                temp = copy.deepcopy(parents[0][:split_at])
                parents[0][:split_at] = copy.deepcopy(parents[1][:split_at])
                parents[1][:split_at] = copy.deepcopy(temp)

            new_population = np.append(new_population, parents, axis = 0)
            n_children += 2

        #Mutate the non-elitist children. Each bit of the genetic code has a probability MR of mutating into the opposite.
        mutation_positions = np.random.choice([1, 0], size=(POP_SIZE, SIZE**2), p=[MR, 1.0-MR])
        mutation_positions[:int(Elitism*POP_SIZE)] = 0
        new_population = np.logical_xor(mutation_positions, new_population)
        population = copy.deepcopy(new_population)


    for i in range(population.shape[0]):
        fitnesses[i] = get_individual_fitness(population[i])
    sorted_inds = fitnesses.argsort()
    population = population[sorted_inds]
    fitnesses = fitnesses[sorted_inds]
    print(fitnesses)

    np.savetxt("Genetic_info.txt", population[-1])




"""
#Run evolution method, accroding to constants defined at the beginning of the script
run_evolution()

to_visualize = np.loadtxt("Genetic_info.txt")
size_organism = int(np.sqrt(to_visualize.shape[0]))
G = Game_of_life(10, 100, to_visualize.reshape((size_organism, size_organism)))
input("Press the Enter key to continue: ")
G.run_animate()
"""
