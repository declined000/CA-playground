import numpy as np

def game_of_life_rule(grid, neighbors):
    """
    Classic Conway's Game of Life.
    """
    alive = grid == 1
    new_grid = np.zeros_like(grid, dtype=np.uint8)

    survive = alive & ((neighbors == 2) | (neighbors == 3))
    born = (~alive) & (neighbors == 3)

    new_grid[survive | born] = 1
    return new_grid
