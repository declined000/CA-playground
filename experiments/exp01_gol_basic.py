from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from ca.core import CellularAutomaton2D
from ca.rules import game_of_life_rule
from ca.viz import grid_to_frame, save_gif, with_trails

def main():
    out_path = Path("media/week01/intro_gol.gif")
    frames = []
    trail = None

    ca = CellularAutomaton2D(
        height=256,
        width=256,
        rule_fn=game_of_life_rule,
        p_alive=0.22,
        seed=7,
    )

    def cb(t, grid):
        nonlocal trail
        trail = with_trails(trail, grid, decay=0.86)
        if t % 1 == 0:    # capture every step
            frames.append(grid_to_frame(trail))

    ca.run(steps=200, callback=cb)

    save_gif(frames, str(out_path), fps=20)
    print("Saved:", out_path)

    # Baseline (no trails)
    out_path2 = Path("media/week01/intro_gol_notrails.gif")
    frames2 = []
    ca = CellularAutomaton2D(
        height=256,
        width=256,
        rule_fn=game_of_life_rule,
        p_alive=0.22,
        seed=7,
    )

    def cb2(t, grid):
        if t % 1 == 0:
            frames2.append(grid_to_frame(grid))

    ca.run(steps=200, callback=cb2)
    save_gif(frames2, str(out_path2), fps=20)
    print("Saved:", out_path2)

if __name__ == "__main__":
    main()


