import hashlib
from html import unescape

from response_diff.config import load_config
from response_diff.jsonio import read_json
from response_diff.models import DiffKind
from response_diff.paths import diff_path
from response_diff.report import MarkdownRenderer, publish_report
from response_diff.runner import SnapshotReplayRunner
from tests.support import config, write_json


def resource_run(project, policy=None):
    policy = load_config(project / "config.json") if policy is None else policy
    return SnapshotReplayRunner(policy).run_files(project / "resources/old_responses.json", project / "resources/new_responses.json")


def test_exact_resource_events(project):
    expected, _ = read_json(project / "tests/expected/resource_default.json", 100000)
    result = resource_run(project)
    assert [result.total, result.changed, result.unchanged, result.diff_count] == expected["summary"]
    actual = [[record.id, diff.scope, diff_path(diff), diff.kind.name, diff.old_present, diff.new_present, diff.old_type, diff.new_type, diff.old_value, diff.new_value] for record in result.records for diff in record.diffs]
    assert actual == expected["events"]
    assert [record.id for record in result.records if not record.diffs] == expected["unchanged"]
    assert [result.counts[kind] for kind in list(DiffKind)[:5]] == [1, 4, 3, 2, 0]
    assert (result.ignored_old, result.ignored_new) == (23, 23)
    assert result.candidates == ()
    assert result.old_sha256 == "736c01d5c26bb4a6aa2e641a3397676823760211c7eebbbba519bfb3bfe008f3"
    assert result.new_sha256 == "3ab810cab06b76fcdf18dd3c3401c2b04804b6d88284f5ba730bf2af10dea3de"


def test_resource_configuration_variants(project):
    result = resource_run(project, config())
    assert (result.total, result.changed, result.unchanged, result.diff_count) == (7, 7, 0, 33)
    assert result.counts[DiffKind.VALUE_CHANGED] == 23
    policy = load_config(project / "config.json").to_dict()
    policy["ignore_fields"].append("*_at")
    result = resource_run(project, config(**policy))
    assert (result.changed, result.unchanged, result.diff_count) == (4, 3, 8)


def test_stable_report_and_protected_resources(project, tmp_path):
    files = (project / "resources/old_responses.json", project / "resources/new_responses.json", project / "config.json")
    before = [hashlib.sha256(path.read_bytes()).hexdigest() for path in files]
    policy = load_config(files[2])
    outputs = []
    for index in range(3):
        result = resource_run(project)
        destination = tmp_path / f"report-{index}.md"
        publish_report(result, policy, project, destination, files)
        outputs.append(destination.read_bytes())
    assert outputs[0] == outputs[1] == outputs[2]
    assert outputs[0] == (project / "tests/expected/resource_default_report.md").read_bytes()
    decoded = unescape(outputs[0].decode("utf-8"))
    assert all(name not in decoded for name in policy.ignore_fields)
    assert [hashlib.sha256(path.read_bytes()).hexdigest() for path in files] == before


def test_input_order_and_self_comparison(project, tmp_path):
    policy = load_config(project / "config.json")
    old, _ = read_json(project / "resources/old_responses.json", 100000)
    new, _ = read_json(project / "resources/new_responses.json", 100000)
    left = write_json(tmp_path / "old.json", old[::-1])
    right = write_json(tmp_path / "new.json", new[::-1])
    original = resource_run(project)
    reordered = SnapshotReplayRunner(policy).run_files(left, right)
    assert original.records == reordered.records
    assert original.counts == reordered.counts
    same = SnapshotReplayRunner(policy).run_files(left, left)
    assert (same.total, same.changed, same.unchanged, same.diff_count) == (7, 0, 7, 0)


def test_candidate_fixture_with_actual_files(project, tmp_path):
    policy = config()
    result = SnapshotReplayRunner(policy).run_files(project / "tests/fixtures/candidates_old.json", project / "tests/fixtures/candidates_new.json")
    assert result.diff_count == 3
    assert len(result.candidates) == 1
    destination = tmp_path / "candidates.md"
    publish_report(result, policy, project, destination, ())
    assert "3/3" in destination.read_text(encoding="utf-8")
    assert "需人工确认" in destination.read_text(encoding="utf-8")
