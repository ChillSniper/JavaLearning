from collections import Counter
from copy import deepcopy
from decimal import Decimal

from hypothesis import given, strategies as st

from response_diff.jsonio import dumps
from response_diff.models import DiffKind
from tests.support import body_diff, config, record, run

text = st.text(alphabet="abcXYZ012_ .[]|\n中文", max_size=12)
scalars = st.one_of(st.none(), st.booleans(), st.integers(-10**30, 10**30), st.decimals(min_value=-1000000, max_value=1000000, places=6, allow_nan=False, allow_infinity=False), text)
json_values = st.recursive(scalars, lambda children: st.one_of(st.lists(children, max_size=5), st.dictionaries(text, children, max_size=5)), max_leaves=20)


@given(json_values)
def test_reflexivity(value):
    assert body_diff(value, value) == ()


@given(json_values, json_values)
def test_direction_symmetry(old, new):
    reverse = {DiffKind.FIELD_ADDED: DiffKind.FIELD_REMOVED, DiffKind.FIELD_REMOVED: DiffKind.FIELD_ADDED}
    forward = body_diff(old, new)
    backward = body_diff(new, old)

    def payload(diff, swap=False):
        return dumps([
            (reverse.get(diff.kind, diff.kind) if swap else diff.kind).name,
            [(s.kind, s.value) for s in (diff.new_path if swap else diff.old_path)],
            [(s.kind, s.value) for s in (diff.old_path if swap else diff.new_path)],
            diff.new_present if swap else diff.old_present,
            diff.old_present if swap else diff.new_present,
            diff.new_type if swap else diff.old_type,
            diff.old_type if swap else diff.new_type,
            diff.new_value if swap else diff.old_value,
            diff.old_value if swap else diff.new_value,
        ])

    assert Counter(payload(diff, True) for diff in forward) == Counter(payload(diff) for diff in backward)


@given(st.lists(json_values, max_size=5), st.lists(json_values, max_size=5))
def test_statistics_conservation(old, new):
    result = run([record(value, str(i)) for i, value in enumerate(old)], [record(value, str(i)) for i, value in enumerate(new)])
    assert result.total == result.changed + result.unchanged == max(len(old), len(new))
    assert sum(result.counts.values()) == result.diff_count


@given(json_values, json_values, json_values)
def test_ignore_invariance(body, old_dynamic, new_dynamic):
    policy = config(ignore_fields=["timestamp"])
    assert body_diff({"data": body, "timestamp": old_dynamic}, {"data": body, "timestamp": new_dynamic}, policy) == ()


@given(st.dictionaries(text, json_values, max_size=8))
def test_object_order_invariance(value):
    assert body_diff(value, dict(reversed(list(value.items())))) == ()


@given(st.lists(scalars, min_size=1, max_size=8))
def test_unordered_permutation_and_counts(values):
    policy = config(arrays={"default_mode": "unordered"})
    assert body_diff(values, values[::-1], policy) == ()
    assert len(body_diff(values, values[:-1], policy)) == 1


@given(st.lists(st.integers(), min_size=2, max_size=8, unique=True), text)
def test_identity_movement(values, changed_value):
    policy = config(arrays={"rules": [{"path": [], "mode": "unordered", "match_key": ["id"]}]})
    old = [{"id": number, "name": "original"} for number in values]
    new = deepcopy(old[::-1])
    new[-1]["name"] = "changed:" + changed_value
    diffs = body_diff(old, new, policy)
    assert len(diffs) == 1
    assert diffs[0].old_path[0].value == 0
    assert diffs[0].new_path[0].value == len(values) - 1


@given(st.integers(-10**20, 10**20))
def test_type_preservation(number):
    assert body_diff(str(number), number)[0].kind == DiffKind.TYPE_CHANGED
    assert body_diff(bool(number), number)[0].kind == DiffKind.TYPE_CHANGED


@given(json_values, json_values)
def test_input_protection(old, new):
    saved = deepcopy((old, new))
    body_diff(old, new)
    assert (old, new) == saved
