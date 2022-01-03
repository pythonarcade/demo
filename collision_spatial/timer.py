import time


class Timer:

    def __init__(self) -> None:
        self.avg = 0
        self._t1 = 0
        self._t2 = 0

    def __enter__(self, *args, **kwards):
        self._t1 = time.perf_counter()

    def __exit__(self, *args, **kwards):
        self._t2 = time.perf_counter()
        self.diff = self._t2 - self._t1
        if self.avg == 0:
            self.avg = self.diff
        else:
            self.avg = (self.avg * 1.9 + self.diff * 0.1) / 2.0
