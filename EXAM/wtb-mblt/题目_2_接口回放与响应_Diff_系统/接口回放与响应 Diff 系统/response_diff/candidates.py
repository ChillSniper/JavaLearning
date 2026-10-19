from collections import defaultdict
from typing import Any

from .arrays import ArrayDiffer
from .config import DiffConfig
from .models import MISSING, DynamicCandidate, FieldObservation, Path, ResponseRecord, index_path, json_type, key_path
from .paths import normalized_path, path_sort_key


class CandidateAnalyzer:
    def __init__(self, config: DiffConfig, arrays: ArrayDiffer):
        self.config = config
        self.arrays = arrays
        self.groups = defaultdict(list)

    def observe(self, record: ResponseRecord, old: Any, new: Any) -> None:
        if not self.config.candidates_enabled:
            return
        observations: dict[Path, FieldObservation] = {}
        blocked = set()
        self.walk(old, new, (), (), observations, blocked)
        self.groups[(record.request_method, record.request_path)].append((observations, blocked))

    def walk(self, old: Any, new: Any, old_path: Path, new_path: Path, observations: dict, blocked: set) -> None:
        path = normalized_path(old_path)
        if old is MISSING or new is MISSING or json_type(old) != json_type(new):
            blocked.add(path)
            return
        kind = json_type(old)
        if kind == "object":
            for key in old.keys() | new.keys():
                self.walk(old.get(key, MISSING), new.get(key, MISSING), key_path(old_path, key), key_path(new_path, key), observations, blocked)
        elif kind == "array":
            match = self.arrays.match(old, new, old_path, new_path)
            if not match.observable or match.removed or match.added or not match.pairs:
                blocked.add(path)
                return
            for i, j in match.pairs:
                self.walk(old[i], new[j], index_path(old_path, i), index_path(new_path, j), observations, blocked)
        else:
            entry = observations.setdefault(path, FieldObservation())
            entry.valid = entry.valid and kind != "null"
            entry.types.add(kind)
            entry.changed = entry.changed and old != new

    def finish(self) -> tuple[DynamicCandidate, ...]:
        result = []
        for (method, request_path), samples in sorted(self.groups.items()):
            if len(samples) < self.config.min_samples:
                continue
            paths = {path for observations, _ in samples for path in observations}
            for path in sorted(paths, key=path_sort_key):
                entries = [observations.get(path) for observations, _ in samples]
                if any(entry is None or not entry.valid or not entry.changed for entry in entries):
                    continue
                if len(set().union(*(entry.types for entry in entries))) != 1:
                    continue
                if any(path[:len(prefix)] == prefix for _, blocked in samples for prefix in blocked):
                    continue
                result.append(DynamicCandidate(method, request_path, path, len(samples), len(samples)))
        return tuple(result)
