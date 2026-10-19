import hashlib
from dataclasses import asdict, dataclass, fields
from fnmatch import fnmatchcase
from pathlib import Path as FilePath
from typing import Any

from .errors import ConfigError
from .jsonio import dumps, read_json
from .models import Path


@dataclass(frozen=True)
class Limits:
    max_file_bytes: int = 20_971_520
    max_records: int = 10_000
    max_depth: int = 100
    max_nodes: int = 1_000_000
    max_array_items: int = 10_000
    max_diff_entries: int = 100_000
    max_report_bytes: int = 52_428_800


@dataclass(frozen=True)
class ArrayRule:
    path: tuple[str | int | None, ...]
    mode: str
    match_key: tuple[str, ...] = ()


@dataclass(frozen=True)
class DiffConfig:
    ignore_fields: tuple[str, ...]
    default_mode: str = "ordered"
    rules: tuple[ArrayRule, ...] = ()
    candidates_enabled: bool = True
    min_samples: int = 3
    limits: Limits = Limits()

    def ignores(self, name: str) -> bool:
        return any(fnmatchcase(name, pattern) for pattern in self.ignore_fields)

    def array_rule(self, path: Path) -> ArrayRule:
        for rule in self.rules:
            if len(rule.path) == len(path) and all(
                (selector is None and segment.kind == "index")
                or (type(selector) is str and segment.kind == "key" and selector == segment.value)
                or (type(selector) is int and segment.kind == "index" and selector == segment.value)
                for selector, segment in zip(rule.path, path)
            ):
                return rule
        return ArrayRule((), self.default_mode)

    def to_dict(self) -> dict:
        return {
            "schema_version": 1,
            "ignore_fields": list(self.ignore_fields),
            "arrays": {
                "default_mode": self.default_mode,
                "rules": [
                    {"path": list(rule.path), "mode": rule.mode,
                     **({"match_key": list(rule.match_key)} if rule.match_key else {})}
                    for rule in self.rules
                ],
            },
            "dynamic_candidates": {"enabled": self.candidates_enabled, "min_samples": self.min_samples},
            "limits": asdict(self.limits),
        }

    @property
    def sha256(self) -> str:
        return hashlib.sha256(dumps(self.to_dict()).encode("utf-8")).hexdigest()


def checked_object(value: Any, allowed: set[str], location: str) -> dict:
    if not isinstance(value, dict):
        raise ConfigError(f"{location} 必须为 object")
    if set(value) - allowed:
        raise ConfigError(f"{location} 含未知配置字段：{sorted(set(value) - allowed)}")
    return value


def positive_integer(value: Any, location: str) -> int:
    if type(value) is not int or value <= 0:
        raise ConfigError(f"{location} 必须为正整数")
    return value


def compatible(left: tuple, right: tuple) -> bool:
    return len(left) == len(right) and all(
        a == b and type(a) is type(b)
        or a is None and (b is None or type(b) is int)
        or b is None and type(a) is int
        for a, b in zip(left, right)
    )


def covers(pattern: tuple, target: tuple) -> bool:
    return compatible(pattern, target) and all(a == b or a is None for a, b in zip(pattern, target))


def parse_config(data: Any) -> DiffConfig:
    data = checked_object(data, {"schema_version", "ignore_fields", "arrays", "dynamic_candidates", "limits"}, "config")
    if type(data.get("schema_version", 1)) is not int or data.get("schema_version", 1) != 1:
        raise ConfigError("schema_version 必须为 1")
    patterns = data.get("ignore_fields")
    if not isinstance(patterns, list) or any(type(p) is not str or not p for p in patterns):
        raise ConfigError("ignore_fields 必须为非空 string 组成的数组，允许空数组")
    if len(patterns) != len(set(patterns)):
        raise ConfigError("ignore_fields 含重复模式")
    for pattern in patterns:
        pattern.encode("utf-8")
    arrays = checked_object(data.get("arrays", {}), {"default_mode", "rules"}, "arrays")
    default_mode = arrays.get("default_mode", "ordered")
    if default_mode not in ("ordered", "unordered"):
        raise ConfigError("arrays.default_mode 无效")
    raw_rules = arrays.get("rules", [])
    if not isinstance(raw_rules, list):
        raise ConfigError("arrays.rules 必须为 array")
    rules = []
    for raw in raw_rules:
        raw = checked_object(raw, {"path", "mode", "match_key"}, "arrays.rules[]")
        path, mode = raw.get("path"), raw.get("mode")
        if not isinstance(path, list) or any(
            not (s is None or type(s) is str or type(s) is int and s >= 0) for s in path
        ):
            raise ConfigError("数组规则 path 必须为 string、非负 int 或 null 组成的数组")
        if mode not in ("ordered", "unordered"):
            raise ConfigError("数组规则 mode 无效")
        match_key = raw.get("match_key", [])
        if "match_key" in raw and (
            mode != "unordered" or not isinstance(match_key, list) or not match_key
            or any(type(key) is not str for key in match_key)
        ):
            raise ConfigError("match_key 必须为非空字段名称数组，mode 必须为 unordered")
        if any(fnmatchcase(key, pattern) for key in match_key for pattern in patterns):
            raise ConfigError("match_key 的字段名称被忽略规则覆盖")
        for selector in path + match_key:
            if isinstance(selector, str):
                selector.encode("utf-8")
        rule = ArrayRule(tuple(path), mode, tuple(match_key))
        if any(compatible(rule.path, existing.path) for existing in rules):
            raise ConfigError("数组规则路径重叠")
        rules.append(rule)
    for rule in rules:
        for index, selector in enumerate(rule.path):
            if type(selector) is int:
                prefix = rule.path[:index]
                parents = [r for r in rules if compatible(r.path, prefix)]
                if any(r.mode == "unordered" for r in parents) or (
                    default_mode == "unordered" and not any(covers(r.path, prefix) for r in parents)
                ):
                    raise ConfigError("unordered 数组内部规则必须使用 null 索引")
    candidate = checked_object(data.get("dynamic_candidates", {}), {"enabled", "min_samples"}, "dynamic_candidates")
    enabled = candidate.get("enabled", True)
    if type(enabled) is not bool:
        raise ConfigError("dynamic_candidates.enabled 必须为 boolean")
    min_samples = positive_integer(candidate.get("min_samples", 3), "min_samples")
    limit_data = checked_object(data.get("limits", {}), {item.name for item in fields(Limits)}, "limits")
    limits = Limits(**{key: positive_integer(value, key) for key, value in limit_data.items()})
    return DiffConfig(tuple(patterns), default_mode, tuple(rules), enabled, min_samples, limits)


def load_config(path: FilePath) -> DiffConfig:
    data, _ = read_json(path, 1_048_576)
    return parse_config(data)
