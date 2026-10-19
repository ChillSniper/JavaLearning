from copy import deepcopy
from decimal import Decimal
from itertools import permutations

import pytest

from response_diff.errors import InputValidationError, LimitExceededError
from response_diff.models import DiffKind, json_type
from response_diff.paths import diff_path, display_path
from tests.support import body_diff, config, record, run


def test_status_and_body():
    result = run([record({"x": 1})], [record({"x": 2}, status=201)])
    assert [diff.kind for diff in result.records[0].diffs] == [DiffKind.STATUS_CHANGED, DiffKind.VALUE_CHANGED]
    assert result.records[0].diffs[0].old_value == 200
    assert result.records[0].diffs[0].new_value == 201
    assert diff_path(result.records[0].diffs[0]) == "response.status"


@pytest.mark.parametrize("old,new", list(permutations([{}, [], "a", 1, True, None], 2)))
def test_all_type_pairs(old, new):
    diffs = body_diff(old, new)
    assert len(diffs) == 1
    assert diffs[0].kind == DiffKind.TYPE_CHANGED
    assert diffs[0].old_type == json_type(old)
    assert diffs[0].new_type == json_type(new)
    assert diff_path(diffs[0]) == "$body"


@pytest.mark.parametrize("old,new", [("128", 128), (True, 1), (False, 0)])
def test_strict_types(old, new):
    assert body_diff({"x": old}, {"x": new})[0].kind == DiffKind.TYPE_CHANGED


@pytest.mark.parametrize("old,new", [(1, 2), ("a", "b"), (True, False), (2**60, 2**60 + 1), (Decimal("0.123456789012345678901"), Decimal("0.123456789012345678902"))])
def test_scalar_values(old, new):
    diff = body_diff(old, new)[0]
    assert diff.kind == DiffKind.VALUE_CHANGED
    assert (diff.old_value, diff.new_value) == (old, new)


@pytest.mark.parametrize("old,new", [(1, Decimal("1.0")), (0, Decimal("-0.0")), (None, None), ({}, {}), ([], []), ("", "")])
def test_equal_values(old, new):
    assert body_diff(old, new) == ()


def test_missing_and_null():
    add = body_diff({}, {"x": None})[0]
    remove = body_diff({"x": None}, {})[0]
    assert (add.kind, add.old_present, add.new_present, add.new_type) == (DiffKind.FIELD_ADDED, False, True, "null")
    assert (remove.kind, remove.old_present, remove.new_present, remove.old_type) == (DiffKind.FIELD_REMOVED, True, False, "null")


def test_subtrees_and_deep_path():
    assert len(body_diff({}, {"a": {"b": [1, 2]}})) == 1
    assert len(body_diff({"a": {"b": [1, 2]}}, {})) == 1
    assert len(body_diff({"a": {"b": [1, 2]}}, {"a": None})) == 1
    assert diff_path(body_diff({"a": {"b": [{"x": 1}]}}, {"a": {"b": [{"x": 2}]}})[0]) == "a.b[0].x"


@pytest.mark.parametrize("key,expected", [("a.b", '["a.b"]'), ("items[0]", '["items[0]"]'), ("", '[""]'), ('a"b', '["a\\"b"]'), ("中文", '["中文"]'), ("/a", '["/a"]')])
def test_special_keys(key, expected):
    assert diff_path(body_diff({key: 1}, {key: 2})[0]) == expected


def test_input_unchanged_and_object_order():
    old, new = {"b": 1, "a": {"x": 2}}, {"a": {"x": 2}, "b": 1}
    saved = deepcopy((old, new))
    assert body_diff(old, new) == ()
    assert (old, new) == saved


def test_numeric_index_sort():
    diffs = body_diff(list(range(12)), [100] * 12)
    assert [diff.old_path[0].value for diff in diffs] == list(range(12))


def test_record_union_and_descriptions():
    result = run([record({}, "a"), record({}, "r", description="旧描述")], [record({}, "b"), record({}, "r", description="新描述")])
    assert (result.total, result.changed, result.unchanged, result.diff_count) == (3, 2, 1, 2)
    assert result.records[0].diffs[0].kind == DiffKind.RECORD_REMOVED
    assert result.records[1].diffs[0].kind == DiffKind.RECORD_ADDED
    assert result.records[2].old_description == "旧描述"
    assert result.records[2].description == "新描述"
    assert run([], []).total == 0
    assert run([], [record({})]).changed == 1


@pytest.mark.parametrize("changes", [{"method": "POST"}, {"path": "/different"}])
def test_identity_mismatch(changes):
    with pytest.raises(InputValidationError, match="不一致"):
        run([record({})], [record({}, **changes)])


def test_diff_limit():
    with pytest.raises(LimitExceededError, match="max_diff_entries"):
        body_diff({"x": 0, "y": 0}, {"x": 1, "y": 1}, config(limits={"max_diff_entries": 1}))
    assert len(body_diff({"x": 0}, {"x": 1}, config(limits={"max_diff_entries": 1}))) == 1
    with pytest.raises(LimitExceededError, match="max_diff_entries"):
        run([record({"x": 0})], [record({"x": 1}, status=201)], config(limits={"max_diff_entries": 1}))
    with pytest.raises(LimitExceededError, match="max_diff_entries"):
        run([], [record({}, "a"), record({}, "b")], config(limits={"max_diff_entries": 1}))


def test_unsupported_runtime_type():
    with pytest.raises(InputValidationError):
        json_type(1.5)
