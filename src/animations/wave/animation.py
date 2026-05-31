import numpy as np

from engine.base import Base

CHARS = " .:-=+*#%@"
_CHAR_BYTES = np.array([ord(c) for c in CHARS], dtype=np.uint8)


class Wave(Base):
    def draw_frame(self, t: float) -> str:
        width, height = self.get_size()

        xs = np.arange(width, dtype=np.float32)
        ys = np.arange(height, dtype=np.float32)
        X, Y = np.meshgrid(xs, ys)

        val = (
            np.sin(X * 0.15 - t * 2.0)
            + np.sin(Y * 0.3 - t * 1.5)
            + np.sin((X + Y) * 0.1 - t)
        )
        idxs = np.clip(((val + 3) / 6 * (len(CHARS) - 1)).astype(np.int32), 0, len(CHARS) - 1)
        char_grid = _CHAR_BYTES[idxs]

        return "\n".join(row.tobytes().decode("ascii") for row in char_grid)
