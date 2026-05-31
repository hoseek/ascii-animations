from engine.base import Base
from engine.fire.wind import Wind
from engine.fire.colors import grid_to_indices, render_row
from animations.firewall.constants import SIM_FPS
from animations.firewall.simulation import FirewallSimulation as Simulation


class Firewall(Base):
    STEP_INTERVAL = 1 / SIM_FPS

    def __init__(self) -> None:
        self._wind = Wind()
        self._sim = Simulation()
        self._last_step_t = 0.0
        self._cached_frame: str = ""

    def draw_frame(self, t: float) -> str:
        width, height = self.get_size()

        updated = False
        if self._sim.grid.shape != (height, width):
            self._sim.reset(width, height)
            for _ in range(height * 2):
                self._sim.step(width, height, self._wind.update(t))
            updated = True
        elif t - self._last_step_t >= self.STEP_INTERVAL:
            self._sim.step(width, height, self._wind.update(t))
            self._last_step_t = t
            updated = True

        if updated:
            color_idxs, char_idxs = grid_to_indices(self._sim.grid)
            self._cached_frame = "\n".join(
                render_row(color_idxs[y], char_idxs[y]) for y in range(height)
            )

        return self._cached_frame
