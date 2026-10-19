import re

from .jsonio import dumps
from .models import DiffEntry, DiffKind, Path, PathSegment

IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
KIND_ORDER = {kind: index for index, kind in enumerate(DiffKind)}


def display_path(path: Path) -> str:
    result = ""
    for segment in path:
        if segment.kind == "index":
            result += f"[{segment.value}]"
        elif segment.kind == "any_index":
            result += "[*]"
        elif IDENTIFIER.fullmatch(segment.value):
            result += ("." if result else "") + segment.value
        else:
            result += "[" + dumps(segment.value) + "]"
    return result or "$body"


def normalized_path(path: Path) -> Path:
    return tuple(PathSegment("any_index", None) if s.kind == "index" else s for s in path)


def path_sort_key(path: Path) -> tuple:
    return tuple((0, s.value) if s.kind == "key" else (1, -1 if s.value is None else s.value) for s in path)


def diff_sort_key(diff: DiffEntry) -> tuple:
    return (
        {"status": 0, "body": 1, "record": 2}[diff.scope],
        path_sort_key(diff.old_path if diff.old_present else diff.new_path),
        KIND_ORDER[diff.kind], path_sort_key(diff.new_path),
    )


def diff_path(diff: DiffEntry) -> str:
    if diff.scope == "status":
        return "response.status"
    if diff.scope == "record":
        return "$record"
    old, new = display_path(diff.old_path), display_path(diff.new_path)
    return old + " → " + new if diff.old_present and diff.new_present and old != new else (
        old if diff.old_present else new
    )
