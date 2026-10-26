# Conway's Game of Life

A Python implementation of **Conway's Game of Life** with animated visualization, predefined patterns, custom initial conditions, and genetic-algorithm-based pattern discovery.

The simulation uses NumPy array operations to efficiently calculate cell updates across the grid.

## Features

- Conway's Game of Life simulation
- Vectorized grid updates using NumPy
- Animated visualization with Matplotlib
- Built-in patterns:
  - Random grid
  - Blinker
  - Glider
  - Spaceship
- Support for custom initial configurations
- Equilibrium and periodic-state detection
- Centre-of-mass tracking
- Genetic algorithm for discovering interesting patterns
- Example initial conditions generated through evolutionary optimization

## How Conway's Game of Life Works

Each cell in the grid is either alive or dead. The state of every cell changes according to the number of living neighbouring cells:

1. A live cell with fewer than two neighbours dies from underpopulation.
2. A live cell with two or three neighbours survives.
3. A live cell with more than three neighbours dies from overpopulation.
4. A dead cell with exactly three neighbours becomes alive.

The grid is represented using:

- `1` for alive cells
- `0` for dead cells

## Project Structure

```text
.
├── Game_of_life.py
├── Run_GoL.py
├── GA_GoL.py
├── Interesting_initial_conditions/
└── README.md
```

### Main files

| File | Description |
| --- | --- |
| `Game_of_life.py` | Contains the main simulation class and update logic. |
| `Run_GoL.py` | Runs and visualizes Game of Life simulations. |
| `GA_GoL.py` | Uses a genetic algorithm to evolve initial grid configurations. |
| `Interesting_initial_conditions/` | Contains example patterns and configurations. |

## Requirements

- Python 3
- NumPy
- Matplotlib

Install the dependencies with:

```bash
pip install numpy matplotlib
```

To export animations using Matplotlib's FFmpeg writer, you may also need to install [FFmpeg](https://ffmpeg.org/).

## Running the Simulation

Run the interactive visualization script:

```bash
python Run_GoL.py
```

The script allows you to choose an initial configuration, such as:

```text
rand
blinker
glider
spaceship
```

The simulation will then be displayed as an animation using Matplotlib.

The animation speed can be adjusted in `Run_GoL.py` by changing the value passed to `run_animate()`:

```python
G.run_animate(100)
```

The value represents the delay between frames in milliseconds.

## Using the Simulation

The main simulation class can be imported directly:

```python
from Game_of_life import Game_of_life

game = Game_of_life(100, 100, "glider")

print(f"Active cells: {game.count_active()}")

game.run_timesteps(50)
game.run_animate(100)
```

### Built-in Initial Conditions

```python
from Game_of_life import Game_of_life

random_game = Game_of_life(100, 100, "rand")
blinker_game = Game_of_life(100, 100, "blinker")
glider_game = Game_of_life(100, 100, "glider")
spaceship_game = Game_of_life(100, 100, "spaceship")
```

### Custom Initial Conditions

Custom patterns can be provided as square NumPy arrays. The pattern is placed in the centre of the simulation grid.

```python
import numpy as np
from Game_of_life import Game_of_life

pattern = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 1],
])

game = Game_of_life(50, 50, pattern)
game.run_animate(100)
```

## Available Methods

| Method | Description |
| --- | --- |
| `update()` | Advance the simulation by one timestep. |
| `run_timesteps(Dt)` | Run the simulation for `Dt` timesteps. |
| `run_animate(interval)` | Display an animated visualization. |
| `count_active()` | Count the number of living cells. |
| `current_com()` | Calculate the centre of mass of the living cells. |
| `run_to_equilibrium()` | Estimate when the system reaches a stable or periodic state. |
| `centre_of_mass(npoints, structure)` | Track and save centre-of-mass data. |

## Genetic Algorithm

`GA_GoL.py` uses a genetic algorithm to search for interesting initial configurations.

Each individual in the population represents a possible starting pattern. Patterns are evaluated using a fitness function and evolved through:

- Selection
- Elitism
- Crossover
- Mutation

The main parameters can be configured at the top of `GA_GoL.py`:

```python
GEN = 10        # Number of generations
POP_SIZE = 50   # Population size
MR = 0.2        # Mutation rate
CR = 0.3        # Crossover rate
Elitism = 0.2   # Fraction of elite individuals
SIZE = 5        # Size of the pattern grid
```

Run the genetic algorithm with:

```bash
python GA_GoL.py
```

The best pattern is saved to:

```text
Genetic_info.txt
```

It is then loaded and displayed as an animation.

### Custom Fitness Functions

The fitness function in `GA_GoL.py` can be changed to optimize different behaviours, including:

- Long-lived patterns
- Maximum population
- Population growth
- Population variance
- Movement across the grid
- Time until equilibrium
- Centre-of-mass velocity

Several example fitness functions are included in the script as commented sections.

## Loading Example Patterns

Patterns stored in `Interesting_initial_conditions/` can be loaded using NumPy:

```python
import numpy as np
from Game_of_life import Game_of_life

pattern_data = np.loadtxt(
    "Interesting_initial_conditions/spider.txt"
)

pattern_size = int(np.sqrt(pattern_data.shape[0]))
pattern = pattern_data.reshape((pattern_size, pattern_size))

game = Game_of_life(50, 50, pattern)
game.run_animate(100)
```

## Boundary Conditions

The simulation uses periodic boundary conditions. When a cell moves beyond one edge of the grid, it reappears on the opposite edge.

This allows moving structures such as gliders and spaceships to continue travelling across the grid.

## Performance

Neighbour counts are calculated using NumPy array rolling operations. The cell update function is vectorized to avoid repeatedly processing every grid cell using nested Python loops.

This provides a significant performance improvement compared with a straightforward cell-by-cell implementation.

## Future Improvements

Possible extensions include:

- Adding more predefined patterns
- Supporting non-square custom patterns
- Adding command-line arguments
- Adding pause and reset controls
- Saving animations automatically
- Supporting alternative boundary conditions
- Improving the genetic algorithm
- Adding automated tests and benchmarks
- Providing example screenshots or videos

## License

No license has currently been specified for this repository.
