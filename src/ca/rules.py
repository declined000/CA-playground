import numpy as np

def game_of_life_rule(grid, neighbors):
     """
     Classic Conway's Game of Life.
     B3/S23 (Born with 3 neighbors, Survive with 2 or 3)
     """
     alive = grid == 1
     new_grid = np.zeros_like(grid, dtype=np.uint8)
 
     survive = alive & ((neighbors == 2) | (neighbors == 3))
     born = (~alive) & (neighbors == 3)
 
     new_grid[survive | born] = 1
     return new_grid


def highlife_rule(grid, neighbors):
     """
     HighLife: B36/S23
     Same as GoL, but dead cells also born with 6 neighbors.
     Produces weird replicators and richer behavior.
     """
     alive = grid == 1
     new_grid = np.zeros_like(grid, dtype=np.uint8)
 
     survive = alive & ((neighbors == 2) | (neighbors == 3))
     born = (~alive) & ((neighbors == 3) | (neighbors == 6))
 
     new_grid[survive | born] = 1
     return new_grid


def seeds_rule(grid, neighbors):
     """
     Seeds: B2/S0
     Cells never survive; only dead cells with exactly 2 neighbors are born.
     Tends to produce exploding 'star' patterns.
     """
     new_grid = np.zeros_like(grid, dtype=np.uint8)
     born = (grid == 0) & (neighbors == 2)
     new_grid[born] = 1
     return new_grid


def chaotic_rule(grid, neighbors):
     """
     A more chaotic variant, tuned to be visibly different.
       - a live cell survives with 3, 4 or 5 neighbors
       - a dead cell is born with 3 or 4 neighbors
     """
     alive = grid == 1
     new_grid = np.zeros_like(grid, dtype=np.uint8)
 
     survive = alive & ((neighbors == 3) | (neighbors == 4) | (neighbors == 5))
     born = (~alive) & ((neighbors == 3) | (neighbors == 4))
 
     new_grid[survive | born] = 1
     return new_grid
