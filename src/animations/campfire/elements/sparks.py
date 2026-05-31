import math
import random

from animations.campfire.constants import (
    SPARK_SPAWN_RATE, SPARK_SPAWN_CHANCE,
    SPARK_LIFE_MIN, SPARK_LIFE_MAX,
    SPARK_VY_MIN, SPARK_VY_MAX, SPARK_VX_RANGE, SPARK_GRAVITY,
    PED_ROWS, PED_ROW_COLORS,
    _LEVELS, COLOR_TABLE,
)
from engine.fire.sparks import Sparks as _BaseSparks


class Sparks(_BaseSparks):
    def __init__(self) -> None:
        super().__init__(
            spawn_chance=SPARK_SPAWN_CHANCE,
            spawn_rate=SPARK_SPAWN_RATE,
            life_min=SPARK_LIFE_MIN,
            life_max=SPARK_LIFE_MAX,
            vy_min=SPARK_VY_MIN,
            vy_max=SPARK_VY_MAX,
            vx_range=SPARK_VX_RANGE,
            gravity=SPARK_GRAVITY,
        )

    def spawn_pop(self, pop_x: int, height: int) -> None:
        spawn_y = float(height - 2)
        for _ in range(5):
            side = random.choice([-1, 1])
            x = float(pop_x + random.randint(-2, 2))
            life = random.randint(6, 14)
            if random.random() < 0.4:
                angle = random.uniform(0.1, 0.5)
                speed = random.uniform(1.0, 2.5)
                vy = abs(math.sin(angle)) * speed
            else:
                angle = random.uniform(-0.3, 0.3)
                speed = random.uniform(1.5, 3.5)
                vy = -abs(math.sin(angle)) * speed - 0.3
            self.spawn(x, spawn_y, side * math.cos(angle) * speed, vy, life)

    def pedestal_map(self, fire_height: int, width: int) -> dict[tuple[int, int], str]:
        result: dict[tuple[int, int], str] = {}
        for s in self._sparks:
            sx, sy = int(round(s.x)), int(round(s.y))
            ped_row = sy - fire_height
            if 0 <= ped_row < PED_ROWS and 0 <= sx < width:
                frac = s.life / s.max_life
                ci = max(0, min(_LEVELS - 1, int(frac * 0.9 * (_LEVELS - 1))))
                char = "*" if frac > 0.6 else "."
                result[(ped_row, sx)] = f"{COLOR_TABLE[ci]}{char}{PED_ROW_COLORS[ped_row % len(PED_ROW_COLORS)]}"
        return result
