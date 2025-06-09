from typing import Optional

from agile_ai.injection.decorators import autowire
from agile_ai.utilities.time_provider import TimeProvider


class ProgressCounter:
    time_provider: TimeProvider = autowire(TimeProvider)
    max_count: int
    count: int
    min_sec_delta: Optional[float]
    last_time_sec: float
    label: str

    def __init__(self, max_count=None, min_sec_delta: Optional[float] = 1.0, label: str = "Progress"):
        self.max_count = max_count
        self.count = 0
        self.min_sec_delta = min_sec_delta
        self.last_time_sec = -100000
        self.label = label

    def __call__(self, msg: str, step: int = 1):
        curr_time_sec = self.time_provider.now()
        sec_delta = curr_time_sec - self.last_time_sec
        self.count += step
        if not self.min_sec_delta or sec_delta > self.min_sec_delta:
            if self.max_count:
                percent = self.count / self.max_count * 100
                count_info_string = f"[{self.count}/{self.max_count}] ({percent:.1f}%)"
            else:
                count_info_string = f"[{self.count}/??]"
            self.print_msg(f"{self.label} {count_info_string}: {msg}")
            self.last_time_sec = curr_time_sec

    # noinspection PyMethodMayBeStatic
    def print_msg(self, msg: str):
        print(msg)
