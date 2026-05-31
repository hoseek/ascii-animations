import random

import numpy as np

from animations.campfire.constants import (
    POP_CHANCE, POP_HEAT_BOOST, POP_DURATION, POP_BURST_WIDTH, PED_WIDTH_DIV,
)
from animations.campfire.elements.sparks import Sparks


class Pop:
    def __init__(self) -> None:
        self._start_t: float | None = None
        self._x: int = 0

    def update(
        self,
        grid: np.ndarray,
        cx: int,
        width: int,
        height: int,
        t: float,
        sparks: Sparks,
    ) -> None:
        ped_half = max(4, width // PED_WIDTH_DIV)

        if self._start_t is not None:
            if t - self._start_t < POP_DURATION:
                fade = 1.0 - (t - self._start_t) / POP_DURATION
                bxl = max(0, self._x - POP_BURST_WIDTH)
                bxr = min(width, self._x + POP_BURST_WIDTH + 1)
                for row in range(min(8, height)):
                    row_fade = fade * (1.0 - row / 8)
                    burst = np.clip(
                        np.random.normal(POP_HEAT_BOOST * row_fade, 0.08, bxr - bxl).astype(np.float32),
                        0, 1,
                    )
                    grid[height - 1 - row, bxl:bxr] = np.maximum(grid[height - 1 - row, bxl:bxr], burst)
            else:
                self._start_t = None
        elif random.random() < POP_CHANCE:
            self._start_t = t
            self._x = random.randint(max(0, cx - ped_half), min(width - 1, cx + ped_half))
            sparks.spawn_pop(self._x, height)
