import importlib
import os
import sys
import time
from pathlib import Path

_ROOTS = frozenset({"animations", "engine"})


def _src_dir() -> Path:
    return Path(__file__).parent.parent


def _max_mtime(src: Path) -> float:
    return max((p.stat().st_mtime for p in src.rglob("*.py")), default=0.0)


def _reload(name: str):
    to_remove = [
        k for k in sys.modules
        if k not in ("engine", "engine.run") and k.split(".")[0] in _ROOTS
    ]
    for k in to_remove:
        del sys.modules[k]
    registry = importlib.import_module("engine.registry")
    return registry.ANIMATIONS[name]()


def start(name: str) -> None:
    from engine.registry import ANIMATIONS

    if name not in ANIMATIONS:
        raise KeyError(f"Unknown animation: {name!r}. Available: {list(ANIMATIONS)}")

    src = _src_dir()
    anim = ANIMATIONS[name]()

    os.system("cls" if os.name == "nt" else "clear")
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    FPS = 120
    CHECK_EVERY = 30  # ~250ms

    last_mtime = _max_mtime(src)
    t = 0.0
    last_frame: str | None = None
    tick = 0

    try:
        while True:
            tick += 1
            if tick % CHECK_EVERY == 0:
                current_mtime = _max_mtime(src)
                if current_mtime != last_mtime:
                    anim = _reload(name)
                    last_mtime = current_mtime
                    last_frame = None

            try:
                frame = anim.draw_frame(t)
            except Exception as e:
                frame = f"\033[2J\033[HError in {name!r}:\n{e}\n"

            if frame is not last_frame:
                sys.stdout.write("\033[H")
                sys.stdout.write(frame)
                sys.stdout.flush()
                last_frame = frame

            t += 1 / FPS
            time.sleep(1 / FPS)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()
