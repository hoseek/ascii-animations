from abc import ABC, abstractmethod

import numpy as np


def _clamped_shift(arr: np.ndarray, wind: int) -> np.ndarray:
    if wind == 0:
        return arr
    width = arr.shape[1]
    out = np.empty_like(arr)
    if wind > 0:
        out[:, :width - wind] = arr[:, wind:]
        out[:, width - wind:] = arr[:, -1:]
    else:
        w = -wind
        out[:, w:] = arr[:, :width - w]
        out[:, :w] = arr[:, :1]
    return out


class FireSimulation(ABC):
    def __init__(self) -> None:
        self.grid = np.zeros((1, 1), dtype=np.float32)

    def reset(self, width: int, height: int) -> None:
        self.grid = np.zeros((height, width), dtype=np.float32)

    @abstractmethod
    def _generate_heat(self, width: int) -> np.ndarray:
        """Returns heat source array of shape (width,)."""
        ...

    @abstractmethod
    def _cooling(self, height: int) -> float:
        """Returns cooling factor per step."""
        ...

    def step(self, width: int, height: int, wind: float) -> None:
        grid = self.grid
        grid[-1] = self._generate_heat(width)

        wind_int = round(wind)
        below1 = _clamped_shift(grid[1:], wind_int)
        below2 = _clamped_shift(np.concatenate([grid[2:], grid[-1:]], axis=0), wind_int)

        left = np.empty_like(below1)
        left[:, 1:] = below1[:, :-1]
        left[:, 0] = below1[:, 0]

        right = np.empty_like(below1)
        right[:, :-1] = below1[:, 1:]
        right[:, -1] = below1[:, -1]

        new_vals = (left + below1 + right + below2) / 4.0
        new_vals -= np.random.random((height - 1, width)).astype(np.float32) * self._cooling(height)
        np.clip(new_vals, 0, 1, out=new_vals)

        new_grid = grid.copy()
        new_grid[:-1] = new_vals
        self.grid = new_grid
