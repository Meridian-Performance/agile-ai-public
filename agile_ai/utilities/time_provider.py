import time

from agile_ai.injection.interfaces import Service


class TimeProvider(Service):
    def now(self) -> float:
        return time.time()
