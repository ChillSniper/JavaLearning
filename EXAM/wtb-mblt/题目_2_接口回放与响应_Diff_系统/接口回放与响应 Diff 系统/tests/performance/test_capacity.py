import json
import statistics
import subprocess
import sys

import pytest


@pytest.mark.performance
@pytest.mark.parametrize("kind,size,mode", [("records", 1000, "ordered"), ("records", 10000, "ordered"), *[("array", size, mode) for size in (1000, 10000) for mode in ("ordered", "unordered", "keyed")]])
def test_capacity(project, tmp_path, kind, size, mode):
    measurements = []
    for repeat in range(3):
        directory = tmp_path / f"repeat-{repeat}"
        child = subprocess.run([sys.executable, "-m", "tests.performance.worker", "--kind", kind, "--size", str(size), "--mode", mode, "--directory", str(directory)], cwd=project, capture_output=True, text=True, encoding="utf-8", timeout=60)
        assert child.returncode == 0, child.stderr
        measurement = json.loads(child.stdout)
        assert measurement["seconds"] < 10
        assert measurement["peak_rss_bytes"] < 512 * 1024 * 1024
        assert measurement["report_bytes"] > 0
        measurements.append(measurement)
    print(json.dumps({"kind": kind, "size": size, "mode": mode, "median_seconds": statistics.median(item["seconds"] for item in measurements), "maximum_peak_rss_bytes": max(item["peak_rss_bytes"] for item in measurements)}, ensure_ascii=False))
