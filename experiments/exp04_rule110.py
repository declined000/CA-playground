import numpy as np
import imageio
from pathlib import Path

# --- Rule 110 mapping ---
# Neighborhood -> Next state
RULE_110 = {
    (1, 1, 1): 0,
    (1, 1, 0): 1,
    (1, 0, 1): 1,
    (1, 0, 0): 0,
    (0, 1, 1): 1,
    (0, 1, 0): 1,
    (0, 0, 1): 1,
    (0, 0, 0): 0,
}


def step_rule110(row: np.ndarray) -> np.ndarray:
    """Single Rule 110 update step with periodic boundary conditions."""
    new = np.zeros_like(row)
    N = len(row)
    for i in range(N):
        left = row[(i - 1) % N]
        center = row[i]
        right = row[(i + 1) % N]
        new[i] = RULE_110[(left, center, right)]
    return new


def generate_rule110_gif(
    width: int = 400,
    steps: int = 1100,
    window_height: int | None = None,
    window_size: int | None = None,
    fps: int = 30,
    seed_pos: int | None = None,
    out_path: str = "media/week02/rule110.gif",
) -> None:
    """
    Generate a Rule 110 space-time diagram GIF.

    Defaults are chosen to roughly match the resolution / feel of rule30.gif:
    - width = 400
    - window_height ~= width
    - ~6 seconds at 30fps
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Initialize row
    row = np.zeros(width, dtype=np.uint8)
    if seed_pos is None:
        seed_pos = width // 2
    row[seed_pos] = 1  # single white cell

    # Precompute timeline (steps x width)
    timeline = np.zeros((steps, width), dtype=np.uint8)
    for t in range(steps):
        timeline[t] = row
        row = step_rule110(row)

    # Resolve window height (default to square crop: width x width)
    if window_size is not None:
        window_height = window_size
    if window_height is None:
        window_height = width

    # Determine frame start indices to create ~5–8s GIF
    max_start = max(0, steps - window_height)
    desired_frames = int(6 * fps)  # ~6 seconds default
    num_frames = min(max_start + 1 if max_start > 0 else steps, desired_frames)
    if max_start == 0:
        # Fewer than window height rows; show growth from top
        starts = np.linspace(0, 0, num_frames, dtype=int)
    else:
        starts = np.linspace(0, max_start, num_frames, dtype=int)

    frames = []
    for s in starts:
        if s == 0 and steps < window_height:
            # Pad on top so total height == window_height
            pad = window_height - steps
            window = np.vstack([np.zeros((pad, width), dtype=np.uint8), timeline[:steps]])
        else:
            e = min(s + window_height, steps)
            window = timeline[s:e]
            if window.shape[0] < window_height:
                pad = window_height - window.shape[0]
                window = np.vstack([np.zeros((pad, width), dtype=np.uint8), window])

        img = (window * 255).astype(np.uint8)
        frame = np.stack([img, img, img], axis=-1)
        frames.append(frame)

    # Save GIF
    imageio.mimsave(out_path, frames, fps=fps)
    print(f"Saved: {out_path.resolve()}")


if __name__ == "__main__":
    generate_rule110_gif()


