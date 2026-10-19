import pytest

from response_diff.config import load_config, parse_config
from response_diff.errors import ConfigError
from response_diff.ignore import IgnorePolicy
from response_diff.models import DiffKind
from response_diff.paths import diff_path
from tests.support import body_diff, config, write_json


@pytest.mark.parametrize("data", [None, [], {}, {"ignore_fields": None}, {"ignore_fields": "x"}, {"ignore_fields": [""]}, {"ignore_fields": [1]}, {"ignore_fields": ["x", "x"]}, {"ignore_fields": [], "unknown": 1}, {"ignore_fields": [], "schema_version": 2}, {"ignore_fields": [], "schema_version": True}])
def test_invalid_config(data):
    with pytest.raises(ConfigError):
        parse_config(data)


@pytest.mark.parametrize("updates", [
    {"arrays": []}, {"arrays": {"unknown": 1}}, {"arrays": {"rules": {}}},
    {"arrays": {"default_mode": "invalid"}}, {"arrays": {"rules": [{}]}},
    {"arrays": {"rules": [{"path": [True], "mode": "ordered"}]}},
    {"arrays": {"rules": [{"path": [-1], "mode": "ordered"}]}},
    {"arrays": {"rules": [{"path": [], "mode": "invalid"}]}},
    {"arrays": {"rules": [{"path": [], "mode": "ordered", "match_key": ["id"]}]}},
    {"arrays": {"rules": [{"path": [], "mode": "unordered", "match_key": []}]}},
    {"arrays": {"rules": [{"path": [], "mode": "unordered", "match_key": [1]}]}},
    {"dynamic_candidates": {"enabled": 1}}, {"dynamic_candidates": {"min_samples": 0}},
    {"limits": {"max_depth": True}}, {"limits": {"max_nodes": -1}}, {"limits": {"unknown": 1}},
])
def test_invalid_options(updates):
    with pytest.raises(ConfigError):
        config(**updates)


def test_overlapping_array_rules():
    with pytest.raises(ConfigError, match="重叠"):
        config(arrays={"rules": [{"path": ["a", None, "b"], "mode": "ordered"}, {"path": ["a", 0, "b"], "mode": "unordered"}]})
    config(arrays={"rules": [{"path": ["a", None, "b"], "mode": "ordered"}, {"path": ["a", "0", "b"], "mode": "unordered"}]})


@pytest.mark.parametrize("pattern", ["id", "i*", "*"])
def test_ignored_identity(pattern):
    with pytest.raises(ConfigError, match="覆盖"):
        config(ignore_fields=[pattern], arrays={"rules": [{"path": [], "mode": "unordered", "match_key": ["id"]}]})


def test_unordered_child_selectors():
    with pytest.raises(ConfigError, match="null"):
        config(arrays={"rules": [{"path": ["a"], "mode": "unordered"}, {"path": ["a", 0, "b"], "mode": "ordered"}]})
    with pytest.raises(ConfigError, match="null"):
        config(arrays={"default_mode": "unordered", "rules": [{"path": [0], "mode": "ordered"}]})
    config(arrays={"default_mode": "unordered", "rules": [{"path": [], "mode": "ordered"}, {"path": [0], "mode": "ordered"}]})


@pytest.mark.parametrize("old,new", [({"timestamp": 1}, {"timestamp": 2}), ({}, {"timestamp": 1}), ({"timestamp": 1}, {}), ({"timestamp": {}}, {"timestamp": [1]})])
def test_ignore_all_changes(old, new):
    assert body_diff(old, new, config(ignore_fields=["timestamp"])) == ()


def test_nested_ignore_and_empty_containers():
    policy = config(ignore_fields=["timestamp", "*_at", "trace?d", "[x]id"])
    old = {"a": [{"timestamp": 1, "created_at": 1, "traceId": 1, "xid": 1}], "timestamp": {"timestamp": 2}}
    new = {"a": [{"timestamp": "x", "updated_at": 2, "traceId": None, "xid": 3}]}
    assert body_diff(old, new, policy) == ()
    engine = IgnorePolicy(policy)
    assert engine.prepare(old) == {"a": [{}]}
    assert engine.hits == 5
    assert len(body_diff([{"timestamp": 1}], [], policy)) == 1


def test_case_sensitive_and_container_values():
    diffs = body_diff({}, {"a": {"traceId": 1, "traceid": 2}}, config(ignore_fields=["traceId"]))
    assert diffs[0].new_value == {"traceid": 2}
    assert body_diff({"traceid": 1}, {"traceid": 2}, config(ignore_fields=["traceId"]))[0].kind == DiffKind.VALUE_CHANGED
    assert body_diff({"a": {"traceId": 1}}, {}, config(ignore_fields=["traceId"]))[0].old_value == {}
    assert body_diff({"a": {"traceId": 1}}, {"a": None}, config(ignore_fields=["traceId"]))[0].old_value == {}


def test_config_file_changes_behavior(tmp_path):
    path = tmp_path / "config.json"
    write_json(path, {"ignore_fields": []})
    before = load_config(path)
    write_json(path, {"ignore_fields": ["x"]})
    after = load_config(path)
    assert len(body_diff({"x": 1}, {"x": 2}, before)) == 1
    assert body_diff({"x": 1}, {"x": 2}, after) == ()
    assert before.sha256 != after.sha256
    assert parse_config(before.to_dict()).sha256 == before.sha256


def test_rules_on_missing_or_changed_type():
    policy = config(arrays={"rules": [{"path": ["a"], "mode": "unordered"}]})
    assert body_diff({}, {}, policy) == ()
    assert body_diff({"a": []}, {"a": {}}, policy)[0].kind == DiffKind.TYPE_CHANGED
    assert diff_path(body_diff({}, {"a": []}, policy)[0]) == "a"
