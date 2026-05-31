import math
import random


class Wind:
    def __init__(
        self,
        duration: float = 3.0,
        amplitude: float = 3.5,
        interval_min: float = 3.0,
        interval_max: float = 8.0,
    ) -> None:
        self._duration = duration
        self._amplitude = amplitude
        self._interval_min = interval_min
        self._interval_max = interval_max
        self._gust_start_t: float | None = None
        self._gust_duration: float = duration
        self._gust_amplitude: float = amplitude
        self._gust_bumps: int = 1
        self._next_gust_t = random.uniform(interval_min, interval_max)
        self._current: float = 0.0
        self._turb: float = 0.0

    @property
    def current(self) -> float:
        return self._current

    def update(self, t: float) -> float:
        self._turb = self._turb * 0.8 + random.gauss(0, self._amplitude * 0.08) * 0.2

        if self._gust_start_t is not None:
            elapsed = t - self._gust_start_t
            if elapsed < self._gust_duration:
                progress = elapsed / self._gust_duration
                base = abs(math.sin(progress * math.pi * self._gust_bumps)) * self._gust_amplitude
                self._current = base + self._turb
            else:
                self._gust_start_t = None
                self._next_gust_t = t + random.uniform(self._interval_min, self._interval_max)
                self._current = self._turb
        elif t >= self._next_gust_t:
            self._gust_start_t = t
            self._gust_duration = random.uniform(self._duration * 0.6, self._duration * 1.6)
            self._gust_amplitude = (
                random.uniform(self._amplitude * 0.4, self._amplitude * 1.3)
                * random.choice([-1, 1])
            )
            self._gust_bumps = random.randint(1, 3)
            self._current = self._turb
        else:
            self._current = self._turb

        return self._current
