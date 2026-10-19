from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from typing import Any

from .config import ArrayRule, DiffConfig
from .errors import InputValidationError
from .models import Path, index_path, json_type, key_path
from .paths import display_path


@dataclass(frozen=True)
class ArrayMatch:
    pairs: tuple[tuple[int, int], ...]
    removed: tuple[int, ...]
    added: tuple[int, ...]
    observable: bool


class ArrayDiffer:
    def __init__(self, config: DiffConfig):
        self.config = config
        self.signatures: dict[tuple[int, Path], Any] = {}

    def identity_index(self, values: list, rule: ArrayRule, path: Path, context: str = "body") -> dict:
        result = {}
        for index, item in enumerate(values):
            location = context + " " + display_path(index_path(path, index))
            if not isinstance(item, dict):
                raise InputValidationError(f"{location}：match_key 数组元素必须为 object")
            value = item
            for key in rule.match_key:
                if not isinstance(value, dict) or key not in value:
                    raise InputValidationError(f"{location}：缺少 match_key 字段 {key!r}")
                value = value[key]
            kind = json_type(value)
            if kind not in ("string", "number", "boolean"):
                raise InputValidationError(f"{location}：match_key 必须为非 null 标量")
            identity = (kind, value)
            if identity in result:
                raise InputValidationError(f"{location}：match_key 身份重复")
            result[identity] = index
        return result

    def validate(self, value: Any, path: Path = (), context: str = "body") -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                self.validate(item, key_path(path, key), context)
        elif isinstance(value, list):
            rule = self.config.array_rule(path)
            if rule.match_key:
                self.identity_index(value, rule, path, context)
            for index, item in enumerate(value):
                self.validate(item, index_path(path, index), context)

    def signature(self, value: Any, path: Path) -> Any:
        kind = json_type(value)
        if kind not in ("object", "array"):
            return kind, value
        cache_key = (id(value), path)
        if cache_key in self.signatures:
            return self.signatures[cache_key]
        if kind == "object":
            result = (kind, tuple((key, self.signature(value[key], key_path(path, key))) for key in sorted(value)))
        else:
            children = [self.signature(item, index_path(path, index)) for index, item in enumerate(value)]
            if self.config.array_rule(path).mode == "unordered":
                result = (kind, frozenset(Counter(children).items()))
            else:
                result = (kind, tuple(children))
        self.signatures[cache_key] = result
        return result

    def match(self, old: list, new: list, old_path: Path, new_path: Path) -> ArrayMatch:
        rule = self.config.array_rule(old_path)
        if rule.mode == "ordered":
            common = min(len(old), len(new))
            return ArrayMatch(tuple((i, i) for i in range(common)), tuple(range(common, len(old))), tuple(range(common, len(new))), True)
        if rule.match_key:
            old_index = self.identity_index(old, rule, old_path)
            new_index = self.identity_index(new, rule, new_path)
            pairs = tuple((index, new_index[key]) for key, index in old_index.items() if key in new_index)
            removed = tuple(index for key, index in old_index.items() if key not in new_index)
            added = tuple(index for key, index in new_index.items() if key not in old_index)
            return ArrayMatch(pairs, removed, added, True)
        positions = defaultdict(deque)
        for index, item in enumerate(new):
            positions[self.signature(item, index_path(new_path, index))].append(index)
        pairs, removed = [], []
        for index, item in enumerate(old):
            queue = positions[self.signature(item, index_path(old_path, index))]
            if queue:
                pairs.append((index, queue.popleft()))
            else:
                removed.append(index)
        added = sorted(index for queue in positions.values() for index in queue)
        return ArrayMatch(tuple(pairs), tuple(removed), tuple(added), False)
