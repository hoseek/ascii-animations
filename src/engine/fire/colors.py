import numpy as np

CHARS = " .,:;*#%@$"
RESET = "\033[0m"
_LEVELS = 64

PALETTE = [
    (0.0,  0,   0,   0  ),
    (0.3,  139, 0,   0  ),
    (0.6,  255, 69,  0  ),
    (0.8,  255, 165, 0  ),
    (1.0,  255, 255, 150),
]


def build_color_table(palette: list[tuple]) -> list[str]:
    table = []
    for i in range(_LEVELS):
        heat = i / (_LEVELS - 1)
        for j in range(len(palette) - 1):
            t0, r0, g0, b0 = palette[j]
            t1, r1, g1, b1 = palette[j + 1]
            if heat <= t1:
                frac = (heat - t0) / (t1 - t0)
                r = int(r0 + frac * (r1 - r0))
                g = int(g0 + frac * (g1 - g0))
                b = int(b0 + frac * (b1 - b0))
                table.append(f"\033[38;2;{r};{g};{b}m")
                break
        else:
            _, r, g, b = palette[-1]
            table.append(f"\033[38;2;{r};{g};{b}m")
    return table


DEFAULT_COLOR_TABLE = build_color_table(PALETTE)


def render_row(color_row: np.ndarray, char_row: np.ndarray) -> str:
    parts: list[str] = []
    prev = -1
    for ci, chi in zip(color_row.tolist(), char_row.tolist()):
        if ci != prev:
            parts.append(DEFAULT_COLOR_TABLE[ci])
            prev = ci
        parts.append(CHARS[chi])
    parts.append(RESET)
    return "".join(parts)


def grid_to_indices(grid: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    color_idxs = (grid * (_LEVELS - 1)).clip(0, _LEVELS - 1).astype(int)
    char_idxs = (grid * (len(CHARS) - 1)).clip(0, len(CHARS) - 1).astype(int)
    return color_idxs, char_idxs
