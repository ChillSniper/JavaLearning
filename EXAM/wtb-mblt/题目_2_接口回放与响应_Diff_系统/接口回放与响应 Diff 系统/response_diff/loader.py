from decimal import Decimal
from pathlib import Path
from typing import Any

from .config import Limits
from .errors import InputValidationError, LimitExceededError
from .jsonio import read_json
from .models import ResponseRecord, Snapshot, json_type

METHODS = frozenset({"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "CONNECT", "TRACE"})


def validate_tree(value: Any, limits: Limits, location: str, check_depth: bool = False) -> None:
    pending = [(value, 0)]
    nodes = 0
    while pending:
        current, depth = pending.pop()
        nodes += 1
        if nodes > limits.max_nodes:
            raise LimitExceededError(f"{location}：超过 max_nodes={limits.max_nodes}")
        if check_depth and depth > limits.max_depth:
            raise LimitExceededError(f"{location}：超过 max_depth={limits.max_depth}")
        kind = json_type(current)
        if kind == "string":
            current.encode("utf-8")
        elif isinstance(current, Decimal) and not current.is_finite():
            raise InputValidationError(f"{location}：number 必须为有限数值")
        elif kind == "object":
            for key, item in current.items():
                if type(key) is not str:
                    raise InputValidationError(f"{location}：字段名称必须为 string")
                key.encode("utf-8")
                pending.append((item, depth + 1))
        elif kind == "array":
            if (depth > 0 or check_depth) and len(current) > limits.max_array_items:
                raise LimitExceededError(f"{location}：超过 max_array_items={limits.max_array_items}")
            pending.extend((item, depth + 1) for item in current)


def validate_records(data: Any, limits: Limits, location: str) -> dict[str, ResponseRecord]:
    if not isinstance(data, list):
        raise InputValidationError(f"{location}：根节点必须为 array")
    if len(data) > limits.max_records:
        raise LimitExceededError(f"{location}：超过 max_records={limits.max_records}")
    validate_tree(data, limits, location)
    records = {}
    for index, item in enumerate(data):
        context = f"{location}[{index}]"
        if not isinstance(item, dict):
            raise InputValidationError(f"{context}：记录必须为 object")
        record_id = item.get("id")
        if type(record_id) is not str or not record_id:
            raise InputValidationError(f"{context}：id 必须为非空 string")
        context += f" id={record_id!r}"
        if record_id in records:
            raise InputValidationError(f"{context}：id 重复")
        if type(item.get("description")) is not str:
            raise InputValidationError(f"{context}：description 必须为 string")
        request, response = item.get("request"), item.get("response")
        if not isinstance(request, dict) or not isinstance(response, dict):
            raise InputValidationError(f"{context}：request、response 必须为 object")
        method, path, status = request.get("method"), request.get("path"), response.get("status")
        if type(method) is not str or method not in METHODS:
            raise InputValidationError(f"{context}：request.method 无效")
        if type(path) is not str or not path.startswith("/"):
            raise InputValidationError(f"{context}：request.path 必须以 / 开始")
        if type(status) is not int or not 100 <= status <= 599:
            raise InputValidationError(f"{context}：response.status 必须为 100～599 的 int")
        if "body" not in response:
            raise InputValidationError(f"{context}：缺少 response.body")
        validate_tree(response["body"], limits, context + " response.body", check_depth=True)
        records[record_id] = ResponseRecord(record_id, item["description"], method, path, status, response["body"])
    return records


def load_snapshot(path: Path, limits: Limits) -> Snapshot:
    data, sha256 = read_json(path, limits.max_file_bytes)
    return Snapshot(validate_records(data, limits, str(path)), sha256)
