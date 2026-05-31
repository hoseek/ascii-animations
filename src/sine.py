import math

WIDTH = 80
HEIGHT = 21


def draw_frame(t):
    mid = HEIGHT // 2
    lines = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            sine_y = round(mid - math.sin(x * 0.2 - t) * (HEIGHT // 2 - 1))
            if y == sine_y:
                row.append("*")
            elif y == mid:
                row.append("-")
            else:
                row.append(" ")
        lines.append("".join(row))
    return "\n".join(lines)
