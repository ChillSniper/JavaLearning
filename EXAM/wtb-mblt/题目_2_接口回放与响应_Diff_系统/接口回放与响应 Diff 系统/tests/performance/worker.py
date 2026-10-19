import argparse
import os
import platform
import time
from pathlib import Path

import psutil

from response_diff.jsonio import dumps
from response_diff.report import publish_report
from response_diff.runner import SnapshotReplayRunner
from tests.support import config, record, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=["records", "array"], required=True)
    parser.add_argument("--size", type=int, required=True)
    parser.add_argument("--mode", default="ordered")
    parser.add_argument("--directory", type=Path, required=True)
    args = parser.parse_args()
    args.directory.mkdir(parents=True, exist_ok=True)
    if args.kind == "records":
        old = [record({"value": i, "type": "1", "timestamp": i}, str(i)) for i in range(args.size)]
        new = [record({"value": i + (i % 3 == 0), "type": 1 if i % 3 == 1 else "1", "timestamp": i + 99}, str(i)) for i in range(args.size)]
        policy = config(ignore_fields=["timestamp"])
        expected = sum(i % 3 != 2 for i in range(args.size))
    else:
        values = [{"id": i, "value": i} for i in range(args.size)]
        changed = [{"id": i, "value": -1 if i == 0 else i} for i in reversed(range(args.size))]
        old, new = [record(values)], [record(changed)]
        rule = {"path": [], "mode": "ordered" if args.mode == "ordered" else "unordered"}
        if args.mode == "keyed":
            rule["match_key"] = ["id"]
        policy = config(arrays={"rules": [rule]})
        expected = args.size * 2 if args.mode == "ordered" else 1 if args.mode == "keyed" else 2
    old_path = write_json(args.directory / "old.json", old)
    new_path = write_json(args.directory / "new.json", new)
    output = args.directory / "report.md"
    started = time.perf_counter()
    result = SnapshotReplayRunner(policy).run_files(old_path, new_path)
    publish_report(result, policy, args.directory, output, (old_path, new_path))
    elapsed = time.perf_counter() - started
    assert result.diff_count == expected
    if os.name == "nt":
        peak = psutil.Process().memory_info().peak_wset
    else:
        import resource
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if platform.system() == "Darwin" else 1024)
    measurements = {
        "kind": args.kind, "size": args.size, "mode": args.mode,
        "seconds": elapsed, "peak_rss_bytes": peak,
        "diffs": result.diff_count, "records": result.total,
        "report_bytes": output.stat().st_size,
        "input_bytes": old_path.stat().st_size + new_path.stat().st_size,
        "python": platform.python_version(), "platform": platform.platform(),
        "cpu": platform.processor(), "logical_cpus": psutil.cpu_count(),
        "physical_memory_bytes": psutil.virtual_memory().total,
    }
    (args.directory / "measurement.json").write_text(dumps(measurements) + "\n", encoding="utf-8")
    print(dumps(measurements))


if __name__ == "__main__":
    main()
