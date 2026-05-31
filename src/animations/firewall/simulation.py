import numpy as np

from engine.fire.simulation import FireSimulation
from animations.firewall.constants import HEAT_MEAN, HEAT_STD, COOLING, TURB_CHANCE, TURB_HEAT


class FirewallSimulation(FireSimulation):
    def _generate_heat(self, width: int) -> np.ndarray:
        heat = np.clip(
            np.random.normal(HEAT_MEAN, HEAT_STD, width).astype(np.float32), 0, 1
        )
        turb_mask = np.random.random(width) < TURB_CHANCE
        heat = np.where(
            turb_mask,
            np.maximum(0, heat - np.random.uniform(0, TURB_HEAT, width).astype(np.float32)),
            heat,
        )
        return heat

    def _cooling(self, height: int) -> float:
        return COOLING / height
