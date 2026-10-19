from typing import Any

from .arrays import ArrayDiffer
from .config import DiffConfig
from .errors import LimitExceededError
from .models import MISSING, DiffEntry, DiffKind, Path, index_path, json_type, key_path
from .paths import diff_sort_key


class DiffBudget:
    def __init__(self, maximum: int):
        self.maximum = maximum
        self.count = 0

    def consume(self) -> None:
        self.count += 1
        if self.count > self.maximum:
            raise LimitExceededError(f"超过 max_diff_entries={self.maximum}")


def make_entry(kind: DiffKind, scope: str, old: Any, new: Any, old_path: Path = (), new_path: Path = ()) -> DiffEntry:
    old_present, new_present = old is not MISSING, new is not MISSING
    return DiffEntry(
        kind, scope, old_path, new_path, old_present, new_present,
        old if old_present else None, new if new_present else None,
        json_type(old) if old_present else None, json_type(new) if new_present else None,
    )


class BodyDiffer:
    def __init__(self, config: DiffConfig, arrays: ArrayDiffer | None = None, budget: DiffBudget | None = None):
        self.arrays = arrays if arrays is not None else ArrayDiffer(config)
        self.budget = budget if budget is not None else DiffBudget(config.limits.max_diff_entries)

    def diff(self, old: Any, new: Any) -> tuple[DiffEntry, ...]:
        entries = []
        self.compare(old, new, (), (), entries)
        return tuple(sorted(entries, key=diff_sort_key))

    def emit(self, kind: DiffKind, old: Any, new: Any, old_path: Path, new_path: Path, entries: list) -> None:
        self.budget.consume()
        entries.append(make_entry(kind, "body", old, new, old_path, new_path))

    def compare(self, old: Any, new: Any, old_path: Path, new_path: Path, entries: list) -> None:
        if old is MISSING:
            self.emit(DiffKind.FIELD_ADDED, old, new, old_path, new_path, entries)
            return
        if new is MISSING:
            self.emit(DiffKind.FIELD_REMOVED, old, new, old_path, new_path, entries)
            return
        old_type, new_type = json_type(old), json_type(new)
        if old_type != new_type:
            self.emit(DiffKind.TYPE_CHANGED, old, new, old_path, new_path, entries)
        elif old_type == "object":
            for key in sorted(old.keys() | new.keys()):
                self.compare(old.get(key, MISSING), new.get(key, MISSING), key_path(old_path, key), key_path(new_path, key), entries)
        elif old_type == "array":
            match = self.arrays.match(old, new, old_path, new_path)
            for i, j in match.pairs:
                self.compare(old[i], new[j], index_path(old_path, i), index_path(new_path, j), entries)
            for i in match.removed:
                self.emit(DiffKind.FIELD_REMOVED, old[i], MISSING, index_path(old_path, i), new_path, entries)
            for j in match.added:
                self.emit(DiffKind.FIELD_ADDED, MISSING, new[j], old_path, index_path(new_path, j), entries)
        elif old != new:
            self.emit(DiffKind.VALUE_CHANGED, old, new, old_path, new_path, entries)
