"""
Animation script for Game_of_life.
Black are alive cells, white are the dead ones.
"""

from Game_of_life import Game_of_life
import time
import numpy as np

#Code as it was implemented in MVP
print('\n' + "To choose intial conditions, you can type:")
print(" - 'rand' for random")
print(" - 'blinker'")
print(" - 'glider'")
print(" - 'spaceship'")
initial_cond = input("Please give initial conditions: ")

#Animation code
N = 100 # grid size
G = Game_of_life(N, N, initial_cond)
print(f"Initiated with {G.count_active()} active cells")
G.run_animate(1) #argument is delay between snapshots in ms
#t1 = time.time()
#G.run_timesteps(1)
#print(time.time() - t1)




"""
#Code to visualize organism called "blinker_wave"
to_visualize = np.loadtxt("interesting_initial_conditions/blinker_wave.txt")
size_organism = int(np.sqrt(to_visualize.shape[0]))

G = Game_of_life(10, 200, to_visualize.reshape((size_organism, size_organism)))
input("Press the Enter key to continue: ")
G.run_animate(50) #argument is delay between snapshots in ms
"""




"""
#Code to visualize organism called "expanding_flower"
to_visualize = np.loadtxt("interesting_initial_conditions/expanding_flower.txt")
size_organism = int(np.sqrt(to_visualize.shape[0]))

G = Game_of_life(50, 50, to_visualize.reshape((size_organism, size_organism)))
input("Press the Enter key to continue: ")
G.run_animate(100) #argument is delay between snapshots in ms
"""




"""
#Code to visualize organism called "almost_symmetric"
to_visualize = np.loadtxt("interesting_initial_conditions/almost_symmetric.txt")
size_organism = int(np.sqrt(to_visualize.shape[0]))

G = Game_of_life(50, 50, to_visualize.reshape((size_organism, size_organism)))
input("Press the Enter key to continue: ")
G.run_animate(100) #argument is delay between snapshots in ms
"""
