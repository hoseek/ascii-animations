import numpy as np

from animations.campfire.constants import (
    HEAT_MEAN, HEAT_STD, COOLING, TURB_WIDTH, TURB_CHANCE, TURB_HEAT, PED_WIDTH_DIV,
)
from engine.fire.simulation import FireSimulation


class CampfireSimulation(FireSimulation):
    def _generate_heat(self, width: int) -> np.ndarray:
        cx = width // 2
        ped_half = max(4, width // PED_WIDTH_DIV)
        heat = np.zeros(width, dtype=np.float32)
        xl, xr = max(0, cx - ped_half), min(width, cx + ped_half + 1)
        xs_local = np.arange(xl, xr, dtype=np.float32)
        sigma = ped_half * 0.75
        envelope = np.exp(-((xs_local - cx) ** 2) / (2 * sigma ** 2)).astype(np.float32)
        raw = np.clip(np.random.normal(HEAT_MEAN, HEAT_STD, xr - xl).astype(np.float32), 0, 1)
        heat[xl:xr] = raw * envelope

        xs = np.arange(width, dtype=np.float32)
        dist = np.maximum(0.0, np.abs(xs - cx) - ped_half)
        outside = dist > 0
        strength = np.maximum(0.0, 1.0 - dist / TURB_WIDTH)
        flares = (np.random.random(width) < TURB_CHANCE) & outside
        turb = flares * strength * np.random.uniform(0, TURB_HEAT, width).astype(np.float32)
        return np.maximum(heat, turb.astype(np.float32))

    def _cooling(self, height: int) -> float:
        return COOLING / height
