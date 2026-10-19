import os
import shutil
import subprocess
import sys

import pytest

from tests.support import record, write_json


def invoke(project, *args):
    return subprocess.run([sys.executable, "-m", "response_diff", *map(str, args)], cwd=project, capture_output=True, text=True, encoding="utf-8", timeout=30)


def test_cli_success_and_exit_codes(project, tmp_path):
    output = tmp_path / "中文 report.md"
    normal = invoke(project, "--output", output)
    assert normal.returncode == 0, normal.stderr
    assert "差异明细：10" in normal.stdout
    assert output.read_bytes() == (project / "tests/expected/resource_default_report.md").read_bytes()
    changed = invoke(project, "--output", output, "--fail-on-diff")
    assert changed.returncode == 3
    same = invoke(project, "--new", "resources/old_responses.json", "--output", output, "--fail-on-diff")
    assert same.returncode == 0
    assert "有差异数：0" in same.stdout


@pytest.mark.parametrize("args,code", [(["--unknown"], 2), (["--old", "missing.json"], 1), (["--config", "missing.json"], 1)])
def test_cli_failure_states(project, tmp_path, args, code):
    output = tmp_path / "report.md"
    output.write_bytes(b"previous complete\n")
    result = invoke(project, *args, "--output", output)
    assert result.returncode == code
    assert result.stderr and "总记录数：" not in result.stdout
    assert output.read_bytes() == b"previous complete\n"


def test_invalid_data_and_input_alias(project, tmp_path):
    old = write_json(tmp_path / "invalid.json", [record({}, status=True)])
    result = invoke(project, "--old", old, "--output", tmp_path / "report.md")
    assert result.returncode == 1 and "response.status" in result.stderr
    before = old.read_bytes()
    alias = invoke(project, "--old", old, "--output", old)
    assert alias.returncode == 1 and old.read_bytes() == before
    wrong = write_json(tmp_path / "config.json", {"ignore_fields": [], "unknown": 1})
    assert invoke(project, "--config", wrong, "--output", tmp_path / "report.md").returncode == 1


def test_project_relative_output(project, tmp_path):
    relative = (tmp_path / "relative.md").relative_to(project)
    result = invoke(project, "--output", relative)
    assert result.returncode == 0
    assert (project / relative).is_file()


def test_powershell_forwarding_and_other_cwd(project, tmp_path):
    shell = shutil.which("pwsh")
    assert shell is not None
    output = tmp_path / "中文 with spaces.md"
    result = subprocess.run([shell, "-NoProfile", "-File", str(project / "run.ps1"), "-Python", sys.executable, "--output", str(output), "--fail-on-diff"], cwd=tmp_path, capture_output=True, text=True, encoding="utf-8", timeout=30)
    assert result.returncode == 3, result.stderr
    assert output.read_bytes() == (project / "tests/expected/resource_default_report.md").read_bytes()
    default = subprocess.run([shell, "-NoProfile", "-File", str(project / "run.ps1"), "--output", str(output)], cwd=tmp_path, capture_output=True, text=True, encoding="utf-8", timeout=30)
    assert default.returncode == 0, default.stderr


def test_powershell_missing_python(project, tmp_path):
    result = subprocess.run([shutil.which("pwsh"), "-NoProfile", "-File", str(project / "run.ps1"), "-Python", str(tmp_path / "missing.exe")], cwd=tmp_path, capture_output=True, text=True, encoding="utf-8", timeout=30)
    assert result.returncode == 1
    assert "缺少 Python" in result.stderr


def test_test_script_runs_real_tests(project, tmp_path):
    result = subprocess.run([shutil.which("pwsh"), "-NoProfile", "-File", str(project / "test.ps1"), "-Python", sys.executable, "tests/unit/test_differ.py", "-k", "test_equal_values", "-q"], cwd=tmp_path, capture_output=True, text=True, encoding="utf-8", timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "6 passed" in result.stdout
    assert "测试证据：" in result.stdout
