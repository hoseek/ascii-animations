import math

from animations.base import Base

CHARS = " .:-=+*#%@"


class Wave(Base):
    def draw_frame(self, t: float) -> str:
        width, height = self.get_size()
        lines = []
        for y in range(height):
            row = []
            for x in range(width):
                val = (
                    math.sin(x * 0.15 - t * 2.0)
                    + math.sin(y * 0.3 - t * 1.5)
                    + math.sin((x + y) * 0.1 - t)
                )
                normalized = (val + 3) / 6
                char = CHARS[int(normalized * (len(CHARS) - 1))]
                row.append(char)
            lines.append("".join(row))
        return "\n".join(lines)
