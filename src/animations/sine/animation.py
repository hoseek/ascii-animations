import numpy as np

from engine.base import Base


class Sine(Base):
    def draw_frame(self, t: float) -> str:
        width, height = self.get_size()
        mid = height // 2

        xs = np.arange(width, dtype=np.float32)
        sine_ys = np.round(mid - np.sin(xs * 0.2 - t) * (height // 2 - 1)).astype(np.int32)

        grid = np.full((height, width), ord(" "), dtype=np.uint8)
        grid[mid, :] = ord("-")
        ys_valid = np.clip(sine_ys, 0, height - 1)
        grid[ys_valid, xs.astype(np.int32)] = ord("*")

        return "\n".join(row.tobytes().decode("ascii") for row in grid)
