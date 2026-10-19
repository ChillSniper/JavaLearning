from collections import Counter
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Any

from .errors import InputValidationError

MISSING = object()


class DiffKind(str, Enum):
    STATUS_CHANGED = "状态码变更"
    FIELD_REMOVED = "字段删除"
    FIELD_ADDED = "字段新增"
    TYPE_CHANGED = "字段类型变更"
    VALUE_CHANGED = "字段值变更"
    RECORD_REMOVED = "记录删除"
    RECORD_ADDED = "记录新增"


@dataclass(frozen=True)
class PathSegment:
    kind: str
    value: str | int | None


Path = tuple[PathSegment, ...]


def key_path(path: Path, key: str) -> Path:
    return path + (PathSegment("key", key),)


def index_path(path: Path, index: int) -> Path:
    return path + (PathSegment("index", index),)


def json_type(value: Any) -> str:
    if value is None:
        return "null"
    if type(value) is bool:
        return "boolean"
    if type(value) is int or isinstance(value, Decimal):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    raise InputValidationError(f"不支持的 JSON 类型：{type(value).__name__}")


@dataclass(frozen=True)
class ResponseRecord:
    id: str
    description: str
    request_method: str
    request_path: str
    status: int
    body: Any


@dataclass(frozen=True)
class Snapshot:
    records: dict[str, ResponseRecord]
    sha256: str


@dataclass(frozen=True)
class DiffEntry:
    kind: DiffKind
    scope: str
    old_path: Path
    new_path: Path
    old_present: bool
    new_present: bool
    old_value: Any
    new_value: Any
    old_type: str | None
    new_type: str | None


@dataclass(frozen=True)
class RecordResult:
    id: str
    description: str
    old_description: str | None
    method: str
    request_path: str
    presence: str
    diffs: tuple[DiffEntry, ...]


@dataclass(frozen=True)
class DynamicCandidate:
    method: str
    request_path: str
    path: Path
    samples: int
    changed: int


@dataclass
class FieldObservation:
    valid: bool = True
    types: set[str] = field(default_factory=set)
    changed: bool = True


@dataclass(frozen=True)
class RunResult:
    records: tuple[RecordResult, ...]
    candidates: tuple[DynamicCandidate, ...]
    old_sha256: str
    new_sha256: str
    config_sha256: str
    ignored_old: int
    ignored_new: int

    @property
    def total(self) -> int:
        return len(self.records)

    @property
    def changed(self) -> int:
        return sum(bool(record.diffs) for record in self.records)

    @property
    def unchanged(self) -> int:
        return self.total - self.changed

    @property
    def counts(self) -> Counter:
        return Counter(diff.kind for record in self.records for diff in record.diffs)

    @property
    def diff_count(self) -> int:
        return sum(len(record.diffs) for record in self.records)
