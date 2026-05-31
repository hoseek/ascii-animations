import math

from animations.base import Base


class Sine(Base):
    def draw_frame(self, t: float) -> str:
        width, height = self.get_size()
        mid = height // 2
        lines = []
        for y in range(height):
            row = []
            for x in range(width):
                sine_y = round(mid - math.sin(x * 0.2 - t) * (height // 2 - 1))
                if y == sine_y:
                    row.append("*")
                elif y == mid:
                    row.append("-")
                else:
                    row.append(" ")
            lines.append("".join(row))
        return "\n".join(lines)
