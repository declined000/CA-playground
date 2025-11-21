from pathlib import Path
import sys
import numpy as np

# Ensure we can import the local package
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from ca.core import CellularAutomaton2D
from ca.rules import (
    game_of_life_rule,
    highlife_rule,
    seeds_rule,
    chaotic_rule,
)
from ca.viz import grid_to_colored_frame, save_gif, upscale_nearest


def main():
    out_path = Path("media/week01/multi_universes.gif")

    height = 128
    width = 128
    steps = 220
    p_alive = 0.15
    seed = 7

    rng = np.random.default_rng(seed)
    base_grid = (rng.random((height, width)) < p_alive).astype(np.uint8)

    ca1 = CellularAutomaton2D(height, width, rule_fn=game_of_life_rule, p_alive=0.0)
    ca2 = CellularAutomaton2D(height, width, rule_fn=highlife_rule,      p_alive=0.0)
    ca3 = CellularAutomaton2D(height, width, rule_fn=seeds_rule,         p_alive=0.0)
    ca4 = CellularAutomaton2D(height, width, rule_fn=chaotic_rule,       p_alive=0.0)

    ca1.grid = base_grid.copy()
    ca2.grid = base_grid.copy()
    ca3.grid = base_grid.copy()
    ca4.grid = base_grid.copy()

    color1 = (1.0, 1.0, 1.0)   # white
    color2 = (0.4, 0.9, 1.0)   # cyan
    color3 = (1.0, 0.5, 0.8)   # pink
    color4 = (0.6, 1.0, 0.4)   # lime

    frames = []

    for _t in range(steps):
        f1 = grid_to_colored_frame(ca1.grid, color1)
        f2 = grid_to_colored_frame(ca2.grid, color2)
        f3 = grid_to_colored_frame(ca3.grid, color3)
        f4 = grid_to_colored_frame(ca4.grid, color4)

        top = np.concatenate([f1, f2], axis=1)
        bottom = np.concatenate([f3, f4], axis=1)
        mosaic = np.concatenate([top, bottom], axis=0)

        frames.append(upscale_nearest(mosaic, scale=4))

        ca1.step()
        ca2.step()
        ca3.step()
        ca4.step()

    save_gif(frames, str(out_path), fps=20)
    print("Saved:", out_path.resolve())


if __name__ == "__main__":
    main()


