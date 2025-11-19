import numpy as np

def count_neighbors(grid: np.ndarray) -> np.ndarray:
    """
    Count 8-neighbors for each cell using wrap-around edges.
    """
    return (
        np.roll(np.roll(grid, 1, 0), 1, 1) +  # up-left
        np.roll(grid, 1, 0) +                 # up
        np.roll(np.roll(grid, 1, 0), -1, 1) + # up-right
        np.roll(grid, -1, 0) +                # down
        np.roll(np.roll(grid, -1, 0), -1, 1) +# down-right
        np.roll(np.roll(grid, -1, 0), 1, 1) + # down-left
        np.roll(grid, 1, 1) +                 # left
        np.roll(grid, -1, 1)                  # right
    )


class CellularAutomaton2D:
    def __init__(self, height, width, rule_fn, p_alive=0.2, seed=None):
        self.height = height
        self.width = width
        self.rule_fn = rule_fn
        rng = np.random.default_rng(seed)
        self.grid = (rng.random((height, width)) < p_alive).astype(np.uint8)

    def step(self):
        neighbors = count_neighbors(self.grid)
        self.grid = self.rule_fn(self.grid, neighbors)

    def run(self, steps, callback=None):
        for t in range(steps):
            if callback is not None:
                callback(t, self.grid)
            self.step()
        if callback is not None:
            callback(steps, self.grid)


