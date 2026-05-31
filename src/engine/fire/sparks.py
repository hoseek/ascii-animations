import random
from dataclasses import dataclass

import numpy as np

from engine.fire.colors import _LEVELS, DEFAULT_COLOR_TABLE


@dataclass(slots=True)
class Spark:
    x: float
    y: float
    vx: float
    vy: float
    life: float
    max_life: float


class Sparks:
    def __init__(
        self,
        spawn_chance: float = 0.1,
        spawn_rate: int = 1,
        life_min: int = 20,
        life_max: int = 50,
        vy_min: float = -1.8,
        vy_max: float = -0.8,
        vx_range: float = 0.3,
        gravity: float = 0.04,
        wind_follow: float = 0.9,
    ) -> None:
        self._spawn_chance = spawn_chance
        self._spawn_rate = spawn_rate
        self._life_min = life_min
        self._life_max = life_max
        self._vy_min = vy_min
        self._vy_max = vy_max
        self._vx_range = vx_range
        self._gravity = gravity
        self._wind_follow = wind_follow
        self._sparks: list[Spark] = []

    def reset(self) -> None:
        self._sparks.clear()

    def spawn(self, x: float, y: float, vx: float, vy: float, life: int) -> None:
        self._sparks.append(Spark(x, y, vx, vy, float(life), float(life)))

    def update(self, grid: np.ndarray, width: int, height: int, wind: float) -> None:
        drift = wind * self._wind_follow
        for s in self._sparks:
            s.x += s.vx + drift
            s.y += s.vy
            s.vy += self._gravity
            s.life -= 1
        self._sparks = [s for s in self._sparks if s.life > 0 and -2 <= s.y < height]

        hot_rows = np.where(grid.max(axis=1) > 0.25)[0]
        if len(hot_rows) == 0:
            return
        flame_top = int(hot_rows.min())
        wind_strength = abs(wind)
        spawn_chance = min(1.0, self._spawn_chance * (1.0 + wind_strength * 0.4))
        if random.random() > spawn_chance:
            return
        hot = np.where(grid[flame_top] > 0.1)[0]
        if len(hot) == 0:
            return
        max_rate = self._spawn_rate + int(wind_strength * 0.4)
        vx_bias = wind * 0.15
        for _ in range(random.randint(1, max_rate)):
            life = random.randint(self._life_min, self._life_max)
            self.spawn(
                float(random.choice(hot)),
                float(flame_top),
                random.uniform(-self._vx_range, self._vx_range) + vx_bias,
                random.uniform(self._vy_min, self._vy_max),
                life,
            )

    def render_map(self, height: int, width: int) -> dict[tuple[int, int], tuple[str, str]]:
        result: dict[tuple[int, int], tuple[str, str]] = {}
        for s in self._sparks:
            sx, sy = int(round(s.x)), int(round(s.y))
            if 0 <= sx < width and 0 <= sy < height:
                frac = s.life / s.max_life
                ci = max(0, min(_LEVELS - 1, int(frac * 0.9 * (_LEVELS - 1))))
                result[(sy, sx)] = (DEFAULT_COLOR_TABLE[ci], "*" if frac > 0.6 else ".")
        return result
