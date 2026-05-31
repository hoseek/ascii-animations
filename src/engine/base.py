import shutil
from abc import ABC, abstractmethod


class Base(ABC):
    @staticmethod
    def get_size() -> tuple[int, int]:
        w, h = shutil.get_terminal_size()
        return w, h - 1

    @abstractmethod
    def draw_frame(self, t: float) -> str:
        ...
