from decimal import Decimal

import pytest

from response_diff.paths import display_path
from tests.support import config, record, run


def samples(old, new, policy=None):
    return run([record(value, str(i)) for i, value in enumerate(old)], [record(value, str(i)) for i, value in enumerate(new)], policy)


def test_candidates_preserve_differences():
    result = samples([{"generated_at": i} for i in range(3)], [{"generated_at": i + 1} for i in range(3)])
    assert result.diff_count == 3
    assert len(result.candidates) == 1
    assert (result.candidates[0].samples, result.candidates[0].changed) == (3, 3)
    assert display_path(result.candidates[0].path) == "generated_at"


@pytest.mark.parametrize("old,new", [
    ([{"x": 1}] * 2, [{"x": 2}] * 2),
    ([{"x": 1}] * 3, [{"x": 2}, {"x": 2}, {"x": 1}]),
    ([{"x": 1}] * 3, [{"x": 2}, {}, {"x": 2}]),
    ([{"x": 1}] * 3, [{"x": 2}, {"x": None}, {"x": 2}]),
    ([{"x": "1"}] * 3, [{"x": 2}] * 3),
    ([{"x": None}] * 3, [{"x": None}] * 3),
    ([{"x": 1}, {"x": "a"}, {"x": 1}], [{"x": 2}, {"x": "b"}, {"x": 2}]),
])
def test_invalid_or_insufficient_candidates(old, new):
    assert samples(old, new).candidates == ()


def test_grouping_and_configuration():
    old = [record({"x": 1}, str(i), path=f"/test/{i}") for i in range(3)]
    new = [record({"x": 2}, str(i), path=f"/test/{i}") for i in range(3)]
    assert run(old, new).candidates == ()
    assert samples([{"x": 1}] * 3, [{"x": 2}] * 3, config(ignore_fields=["x"])).candidates == ()
    assert samples([{"x": 1}] * 3, [{"x": 2}] * 3, config(dynamic_candidates={"enabled": False})).diff_count == 3
    assert samples([{"x": 1}] * 2, [{"x": 2}] * 2, config(dynamic_candidates={"min_samples": 2})).candidates[0].samples == 2


def test_array_observation_once_per_record():
    old = [{"items": [{"x": 1}, {"x": 2}]}] * 3
    new = [{"items": [{"x": 3}, {"x": 4}]}] * 3
    result = samples(old, new)
    assert len(result.candidates) == 1
    assert result.candidates[0].samples == 3
    assert display_path(result.candidates[0].path) == "items[*].x"


@pytest.mark.parametrize("replacement", [[], [{"x": 3}], [{"x": 3}, {}], [{"x": 3}, {"x": 2}], [{"x": 3}, {"x": "4"}], [{"x": 3}, {"x": 4}, {"x": 5}]])
def test_incomplete_array_observation(replacement):
    assert samples([{"items": [{"x": 1}, {"x": 2}]}] * 3, [{"items": replacement}] * 3).candidates == ()


def test_unordered_candidate_rules():
    old = [[{"id": 1, "x": 1}, {"id": 2, "x": 2}]] * 3
    new = [[{"id": 2, "x": 4}, {"id": 1, "x": 3}]] * 3
    assert samples(old, new, config(arrays={"default_mode": "unordered"})).candidates == ()
    keyed = config(arrays={"rules": [{"path": [], "mode": "unordered", "match_key": ["id"]}]})
    result = samples(old, new, keyed)
    assert len(result.candidates) == 1
    assert display_path(result.candidates[0].path) == "[*].x"


def test_container_change_blocks_nested_candidate():
    assert samples([{"a": {"x": 1}}] * 3, [{"a": {"x": 2}}, {"a": None}, {"a": {"x": 2}}]).candidates == ()
    assert samples([1, Decimal("1.0"), 1], [2, Decimal("2.0"), 2]).candidates[0].samples == 3
