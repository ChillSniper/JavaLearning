from decimal import Decimal

import pytest

from response_diff.errors import InputValidationError
from response_diff.models import DiffKind
from response_diff.paths import diff_path
from tests.support import body_diff, config, record, run


def unordered(key=None):
    rule = {"path": [], "mode": "unordered"}
    if key is not None:
        rule["match_key"] = key
    return config(arrays={"rules": [rule]})


def test_ordered_changes():
    assert diff_path(body_diff([1], [1, 2])[0]) == "[1]"
    assert body_diff([1, 2], [1])[0].kind == DiffKind.FIELD_REMOVED
    assert len(body_diff([1, 2], [2, 1])) == 2
    assert diff_path(body_diff([{"x": 1}], [{"x": 2}])[0]) == "[0].x"


def test_unordered_counts_and_types():
    policy = unordered()
    assert body_diff([1, 1, 2], [2, 1, 1], policy) == ()
    assert body_diff([1, Decimal("1.0"), 2], [2, 1, 1], policy) == ()
    assert len(body_diff([1, 1, 2], [1, 2], policy)) == 1
    assert len(body_diff([1, 2], [1, 1, 2], policy)) == 1
    assert len(body_diff([True, "1"], [1, 1], policy)) == 4
    assert body_diff([Decimal("-0")], [0], policy) == ()
    assert body_diff([None, [], {}], [{}, None, []], policy) == ()


def test_unordered_objects():
    assert body_diff([{"a": 1, "b": 2}], [{"b": 2, "a": 1}], unordered()) == ()
    diffs = body_diff([{"a": 1}], [{"a": 2}], unordered())
    assert {diff.kind for diff in diffs} == {DiffKind.FIELD_ADDED, DiffKind.FIELD_REMOVED}
    assert {diff_path(diff) for diff in diffs} == {"[0]"}
    ignored = config(ignore_fields=["timestamp"], arrays={"default_mode": "unordered"})
    assert body_diff([{"id": 1, "timestamp": 1}, {"id": 2, "timestamp": 2}], [{"id": 2, "timestamp": 99}, {"id": 1}], ignored) == ()


def test_keyed_reorder_and_paths():
    old = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}]
    assert body_diff(old, list(reversed(old)), unordered(["id"])) == ()
    new = [{"id": 2, "name": "b"}, {"id": 1, "name": "c"}]
    diffs = body_diff(old, new, unordered(["id"]))
    assert len(diffs) == 1
    assert diff_path(diffs[0]) == "[0].name → [1].name"
    diffs = body_diff(old, [{"id": 3}], unordered(["id"]))
    assert len(diffs) == 3
    assert sum(diff.kind == DiffKind.FIELD_REMOVED for diff in diffs) == 2


@pytest.mark.parametrize("values", [[1], [{}], [{"id": None}], [{"id": {}}], [{"id": []}], [{"id": 1}, {"id": 1}], [{"id": 1}, {"id": Decimal("1.0")}], [{"id": True}, {"id": True}]])
def test_invalid_identity(values):
    with pytest.raises(InputValidationError, match="match_key"):
        body_diff(values, values, unordered(["id"]))


def test_distinct_identity_types_and_nested_key():
    values = [{"id": "1"}, {"id": 1}, {"id": True}]
    assert body_diff(values, values[::-1], unordered(["id"])) == ()
    values = [{"user": {"id": 1}}, {"user": {"id": 2}}]
    assert body_diff(values, values[::-1], unordered(["user", "id"])) == ()


def test_nested_modes_and_null_selector():
    policy = config(arrays={"rules": [
        {"path": ["groups"], "mode": "unordered", "match_key": ["id"]},
        {"path": ["groups", None, "members"], "mode": "unordered"},
    ]})
    old = {"groups": [{"id": 1, "members": [1, 2]}, {"id": 2, "members": [3, 4]}]}
    new = {"groups": [{"id": 2, "members": [4, 3]}, {"id": 1, "members": [2, 1]}]}
    assert body_diff(old, new, policy) == ()
    assert len(body_diff([[1, 2]], [[2, 1]], unordered())) == 2
    assert body_diff([[1, 2]], [[2, 1]], config(arrays={"default_mode": "unordered"})) == ()
    special = config(arrays={"rules": [{"path": ["a.b"], "mode": "unordered"}]})
    assert body_diff({"a.b": [1, 2]}, {"a.b": [2, 1]}, special) == ()


def test_added_container_prevalidation():
    policy = config(arrays={"rules": [{"path": ["items"], "mode": "unordered", "match_key": ["id"]}]})
    with pytest.raises(InputValidationError, match="match_key"):
        run([], [record({"items": [{}]})], policy)
