import time
import os
import sys
import importlib
import inspect
from animations.base import Base


def _find_animation(module) -> Base:
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, Base) and obj is not Base:
            return obj()
    raise RuntimeError(f"No Animation subclass found in {module.__name__}")


def start(module_name: str) -> None:
    module = importlib.import_module(module_name)
    module_file = module.__file__
    assert module_file is not None

    os.system("cls" if os.name == "nt" else "clear")
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    last_mtime = os.path.getmtime(module_file)
    anim = _find_animation(module)
    t = 0.0

    try:
        while True:
            current_mtime = os.path.getmtime(module_file)
            if current_mtime != last_mtime:
                importlib.reload(module)
                anim = _find_animation(module)
                last_mtime = current_mtime

            sys.stdout.write("\033[H")
            try:
                sys.stdout.write(anim.draw_frame(t))
            except Exception as e:
                sys.stdout.write(f"\033[2J\033[HError in {module_file}:\n{e}\n")

            sys.stdout.flush()
            t += 0.05
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()
