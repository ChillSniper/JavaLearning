from pathlib import Path

from .arrays import ArrayDiffer
from .candidates import CandidateAnalyzer
from .config import DiffConfig
from .differ import BodyDiffer, DiffBudget, make_entry
from .errors import InputValidationError
from .ignore import IgnorePolicy
from .loader import load_snapshot
from .models import MISSING, DiffKind, RecordResult, RunResult, Snapshot
from .paths import diff_sort_key


class SnapshotReplayRunner:
    def __init__(self, config: DiffConfig):
        self.config = config

    def run_files(self, old_path: Path, new_path: Path) -> RunResult:
        old = load_snapshot(old_path, self.config.limits)
        new = load_snapshot(new_path, self.config.limits)
        return self.compare(old, new)

    def compare(self, old: Snapshot, new: Snapshot) -> RunResult:
        for record_id in old.records.keys() & new.records.keys():
            left, right = old.records[record_id], new.records[record_id]
            if (left.request_method, left.request_path) != (right.request_method, right.request_path):
                raise InputValidationError(f"id={record_id!r}：request.method 或 request.path 不一致")
        old_policy, new_policy = IgnorePolicy(self.config), IgnorePolicy(self.config)
        old_bodies = {key: old_policy.prepare(record.body) for key, record in old.records.items()}
        new_bodies = {key: new_policy.prepare(record.body) for key, record in new.records.items()}
        arrays = ArrayDiffer(self.config)
        for side, bodies in (("old", old_bodies), ("new", new_bodies)):
            for record_id, body in bodies.items():
                arrays.validate(body, context=f"{side} id={record_id!r}")
        budget = DiffBudget(self.config.limits.max_diff_entries)
        differ, analyzer = BodyDiffer(self.config, arrays, budget), CandidateAnalyzer(self.config, arrays)
        results = []
        for record_id in sorted(old.records.keys() | new.records.keys()):
            left, right = old.records.get(record_id), new.records.get(record_id)
            record = right if right is not None else left
            entries = []
            if left is None or right is None:
                value = {"status": record.status, "body": (new_bodies if left is None else old_bodies)[record_id]}
                budget.consume()
                entries.append(make_entry(
                    DiffKind.RECORD_ADDED if left is None else DiffKind.RECORD_REMOVED,
                    "record", MISSING if left is None else value, value if left is None else MISSING,
                ))
            else:
                if left.status != right.status:
                    budget.consume()
                    entries.append(make_entry(DiffKind.STATUS_CHANGED, "status", left.status, right.status))
                entries.extend(differ.diff(old_bodies[record_id], new_bodies[record_id]))
                analyzer.observe(record, old_bodies[record_id], new_bodies[record_id])
            results.append(RecordResult(
                record_id, record.description,
                left.description if left is not None and right is not None and left.description != right.description else None,
                record.request_method, record.request_path,
                "new_only" if left is None else "old_only" if right is None else "both",
                tuple(sorted(entries, key=diff_sort_key)),
            ))
        return RunResult(tuple(results), analyzer.finish(), old.sha256, new.sha256, self.config.sha256, old_policy.hits, new_policy.hits)
