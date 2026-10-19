import hashlib
from pathlib import Path
from typing import Any

import simplejson

from .errors import InputValidationError, LimitExceededError


def dumps(value: Any) -> str:
    return simplejson.dumps(
        value, use_decimal=True, ensure_ascii=False, sort_keys=True,
        allow_nan=False, separators=(",", ":"),
    )


def read_json(path: Path, max_bytes: int) -> tuple[Any, str]:
    with path.open("rb") as stream:
        content = stream.read(max_bytes + 1)
    if len(content) > max_bytes:
        raise LimitExceededError(f"{path}：超过 max_file_bytes={max_bytes}")

    def unique_object(pairs: list[tuple[str, Any]]) -> dict:
        result = {}
        for key, value in pairs:
            if key in result:
                raise InputValidationError(f"{path}：JSON 字段名称重复 {key!r}")
            result[key] = value
        return result

    data = simplejson.loads(
        content.decode("utf-8-sig"), use_decimal=True, allow_nan=False,
        object_pairs_hook=unique_object,
    )
    return data, hashlib.sha256(content).hexdigest()
