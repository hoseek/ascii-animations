from animations.campfire.constants import PED_ROWS, PED_WIDTH_DIV, PED_ROW_COLORS, RESET


def build_grid(width: int) -> list[list[str]]:
    cx = width // 2
    top_half = max(4, width // PED_WIDTH_DIV)
    step = 2
    grid = []
    for i in range(PED_ROWS):
        half = top_half + i * step
        xl, xr = cx - half, cx + half
        row = [" "] * width
        fill_l, fill_r = max(0, xl + 1), min(width, xr)
        if i % 2 == 0:
            for x in range(fill_l, fill_r):
                row[x] = "=" if (x - fill_l) % 6 == 0 else "#"
        else:
            brick_offset = (i // 2) % 2 * 3
            for x in range(fill_l, fill_r):
                row[x] = ":" if (x - fill_l + brick_offset) % 5 == 0 else "#"
        if 0 <= xl < width:
            row[xl] = "|" if i not in (0, PED_ROWS - 1) else "+"
        if 0 <= xr < width:
            row[xr] = "|" if i not in (0, PED_ROWS - 1) else "+"
        if i == 0:
            for x in range(max(0, xl), min(width, xr + 1)):
                if row[x] != "+":
                    row[x] = "="
        grid.append(row)
    return grid


def render_grid(grid: list[list[str]]) -> list[str]:
    lines = []
    for i, row in enumerate(grid):
        color = PED_ROW_COLORS[i % len(PED_ROW_COLORS)]
        lines.append(f"{color}{''.join(row)}{RESET}")
    return lines
