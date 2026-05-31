import math

WIDTH = 80
HEIGHT = 24
CHARS = " .:-=+*#%@"


def draw_frame(t):
    lines = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
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
