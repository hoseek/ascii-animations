from engine.base import Base
from animations.campfire import pedestal
from animations.campfire.constants import COLOR_TABLE, PED_ROWS, SIM_FPS
from animations.campfire.elements.pop import Pop
from animations.campfire.elements.simulation import CampfireSimulation as Simulation
from animations.campfire.elements.sparks import Sparks
from animations.campfire.elements.wind import Wind
from engine.fire.colors import CHARS, RESET, grid_to_indices, render_row


class Fire(Base):
    STEP_INTERVAL = 1 / SIM_FPS

    def __init__(self) -> None:
        self._wind = Wind()
        self._sparks = Sparks()
        self._pop = Pop()
        self._sim = Simulation()
        self._last_step_t = 0.0
        self._cached_frame: str = ""

    def draw_frame(self, t: float) -> str:
        width, height = self.get_size()
        fire_height = height - PED_ROWS

        updated = False
        if self._sim.grid.shape != (fire_height, width):
            self._sim.reset(width, fire_height)
            self._sparks.reset()
            for _ in range(fire_height * 2):
                self._sim.step(width, fire_height, self._wind.update(t))
            updated = True
        elif t - self._last_step_t >= self.STEP_INTERVAL:
            wind = self._wind.update(t)
            self._pop.update(self._sim.grid, width // 2, width, fire_height, t, self._sparks)
            self._sim.step(width, fire_height, wind)
            self._sparks.update(self._sim.grid, width, fire_height + PED_ROWS, wind)
            self._last_step_t = t
            updated = True

        if updated:
            grid = self._sim.grid
            color_idxs, char_idxs = grid_to_indices(grid)

            lines = [render_row(color_idxs[y], char_idxs[y]) for y in range(fire_height)]

            spark_map = self._sparks.render_map(fire_height, width)
            for y in {sy for sy, _ in spark_map}:
                parts: list[str] = []
                prev = -1
                for x in range(width):
                    if (y, x) in spark_map:
                        color, char = spark_map[(y, x)]
                        parts.append(color + char)
                        prev = -1
                    else:
                        ci = color_idxs[y, x]
                        if ci != prev:
                            parts.append(COLOR_TABLE[ci])
                            prev = ci
                        parts.append(CHARS[char_idxs[y, x]])
                parts.append(RESET)
                lines[y] = "".join(parts)

            ped_grid = pedestal.build_grid(width)
            for (ped_row, sx), cell in self._sparks.pedestal_map(fire_height, width).items():
                ped_grid[ped_row][sx] = cell
            lines.extend(pedestal.render_grid(ped_grid))

            self._cached_frame = "\n".join(lines)

        return self._cached_frame
