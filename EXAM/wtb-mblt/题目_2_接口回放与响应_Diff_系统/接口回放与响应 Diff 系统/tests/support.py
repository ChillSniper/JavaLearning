import hashlib
from pathlib import Path

from response_diff.config import parse_config
from response_diff.ignore import IgnorePolicy
from response_diff.jsonio import dumps
from response_diff.loader import validate_records
from response_diff.models import Snapshot
from response_diff.runner import SnapshotReplayRunner


def record(body, record_id="r", status=200, method="GET", path="/test", description="测试请求"):
    return {"id": record_id, "description": description, "request": {"method": method, "path": path}, "response": {"status": status, "body": body}}


def config(**updates):
    return parse_config({"ignore_fields": [], **updates})


def snapshot(rows, policy):
    return Snapshot(validate_records(rows, policy.limits, "测试输入"), hashlib.sha256(dumps(rows).encode("utf-8")).hexdigest())


def run(old, new, policy=None):
    policy = policy if policy is not None else config()
    return SnapshotReplayRunner(policy).compare(snapshot(old, policy), snapshot(new, policy))


def body_diff(old, new, policy=None):
    return run([record(old)], [record(new)], policy).records[0].diffs


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dumps(value), encoding="utf-8", newline="\n")
    return path


def ignored(value, policy):
    return IgnorePolicy(policy).prepare(value)
