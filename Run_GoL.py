"""
Animation script for Game_of_life.
Black are alive cells, white are the dead ones.
"""

from Game_of_life import Game_of_life
import time

print('\n' + "To choose intial conditions, you can type:")
print(" - 'rand' for random")
print(" - 'blinker'")
print(" - 'glider'")
print(" - 'spaceship'")
initial_cond = input("Please give initial conditions: ")

#Animation code
N = 200 # grid size
G = Game_of_life(N, initial_cond)
print(f"Initiated with {G.count_active()} active cells")
G.run_animate()
