import imageio
import numpy as np
import os

def grid_to_frame(grid):
    """
    Convert 0/1 grid -> grayscale RGB image.
    """
    img = (grid * 255).astype(np.uint8)
    return np.stack([img, img, img], axis=-1)

def grid_to_colored_frame(grid, color=(1.0, 1.0, 1.0)):
    """
    Convert 0/1 grid -> tinted RGB image. color is (r,g,b) in 0–1.
    """
    base = grid.astype(np.float32)[..., None]
    rgb = base * np.array(color, dtype=np.float32)[None, None, :]
    return (rgb * 255).astype(np.uint8)

def upscale_nearest(frame, scale=4):
    """
    Nearest-neighbor upscale for crisp pixel art visuals.
    """
    return np.repeat(np.repeat(frame, scale, axis=0), scale, axis=1)

def save_gif(frames, out_path, fps=20):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    imageio.mimsave(out_path, frames, fps=fps)


def with_trails(prev_intensity, grid, decay=0.86):
    """
    Exponential decay intensity buffer for motion trails.
    - prev_intensity: previous float32 buffer in [0,1] or None
    - grid: current 0/1 grid
    - decay: multiplier applied to previous intensity
    Returns a float32 buffer in [0,1].
    """
    current = grid.astype(np.float32)
    if prev_intensity is None:
        return current
    if prev_intensity.shape != current.shape:
        prev_intensity = np.zeros_like(current, dtype=np.float32)
    return np.maximum(current, prev_intensity * decay)

