from functools import lru_cache
from typing import Any

from .config import DiffConfig


class IgnorePolicy:
    def __init__(self, config: DiffConfig):
        self.matches = lru_cache(maxsize=4096)(config.ignores)
        self.hits = 0

    def prepare(self, value: Any) -> Any:
        if isinstance(value, dict):
            result = {}
            for key, item in value.items():
                if self.matches(key):
                    self.hits += 1
                else:
                    result[key] = self.prepare(item)
            return result
        if isinstance(value, list):
            return [self.prepare(item) for item in value]
        return value
