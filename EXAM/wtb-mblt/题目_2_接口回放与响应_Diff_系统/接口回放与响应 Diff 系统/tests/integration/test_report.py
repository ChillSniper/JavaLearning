from html import unescape
from pathlib import Path
import os

import pytest
from markdown_it import MarkdownIt

from response_diff.errors import InputValidationError, LimitExceededError
from response_diff.models import DiffKind
from response_diff.report import MarkdownRenderer, ReportWriter, publish_report
from tests.support import config, record, run


def test_markdown_escaping_and_full_values():
    text = '竖线|反引号`换行\n<script>x</script> [link](https://example.org) ![x](x) *a* _b_ \\ '
    long_value = text + "长内容" * 1000
    result = run([record({text: 1}, description=text + "\x00\x0b\x0c")], [record({text: long_value}, description=text + "\x00\x0b\x0c")])
    content = MarkdownRenderer().render(result, 1000000)
    tokens = MarkdownIt("commonmark").enable("table").parse(content.decode("utf-8"))
    assert not any(token.type in ("html_inline", "html_block", "link_open", "image", "em_open", "strong_open") for item in tokens for token in [item, *(item.children or [])])
    body_rows = []
    current = None
    for token in tokens:
        if token.type == "tr_open":
            current = []
        elif token.type == "td_open":
            current.append("cell")
        elif token.type == "tr_close" and current:
            body_rows.append(len(current))
    assert 5 in body_rows
    assert long_value.replace("\n", "\\n") in unescape(content.decode("utf-8")).replace("\\\\", "\\")
    assert content.endswith(b"\n") and b"\r\n" not in content
    assert b"\x00" not in content and b"\x0b" not in content and b"\x0c" not in content
    assert "\\x00\\x0b\\x0c" in unescape(content.decode("utf-8"))


def test_complete_values_and_scopes():
    result = run([record({"response": {"status": 1}, "a": None})], [record({"response": {"status": 2}, "b": True}, status=201)])
    content = MarkdownRenderer().render(result, 100000).decode("utf-8")
    assert "| HTTP | response.status" in content
    assert "| body | response.status" in content
    assert "null" in content and "boolean true" in content
    assert "字段不存在" in content


def test_empty_and_record_reports():
    empty = MarkdownRenderer().render(run([], []), 100000).decode("utf-8")
    assert "差异记录数量：0" in empty
    changed = run([record({"x": 1}, "a")], [record({"x": 2}, "b")])
    content = MarkdownRenderer().render(changed, 100000).decode("utf-8")
    assert "$record" in content and '"body":{"x":1}' in content
    assert changed.counts[DiffKind.RECORD_ADDED] == changed.counts[DiffKind.RECORD_REMOVED] == 1
    desc = run([record({}, description="旧描述")], [record({}, description="新描述")])
    assert "旧版描述：旧描述" in MarkdownRenderer().render(desc, 100000).decode("utf-8")
    desc = run([record({"x": 1}, description="旧描述")], [record({"x": 2}, description="新描述")])
    assert "旧版描述：旧描述" in MarkdownRenderer().render(desc, 100000).decode("utf-8")


def test_report_size_boundary():
    result = run([], [])
    content = MarkdownRenderer().render(result, 100000)
    assert MarkdownRenderer().render(result, len(content)) == content
    with pytest.raises(LimitExceededError, match="max_report_bytes"):
        MarkdownRenderer().render(result, len(content) - 1)


def test_atomic_output_and_failures(tmp_path):
    writer = ReportWriter(tmp_path)
    protected = tmp_path / "input.json"
    protected.write_bytes(b"[]")
    with pytest.raises(InputValidationError, match="相同"):
        writer.prepare(protected, (protected,))
    alias = tmp_path / "alias.md"
    os.link(protected, alias)
    with pytest.raises(InputValidationError, match="相同"):
        writer.prepare(alias, (protected,))
    output = writer.prepare(tmp_path / "new/output.md", (protected,))
    writer.write(output, b"complete\n")
    assert output.read_bytes() == b"complete\n"
    directory = writer.prepare(tmp_path / "directory", ())
    directory.mkdir()
    with pytest.raises(OSError):
        writer.write(directory, b"new\n")
    assert output.read_bytes() == b"complete\n"
    assert protected.read_bytes() == b"[]"
    assert not list(writer.staging.glob("*.tmp")) == []


def test_size_failure_keeps_previous_report(tmp_path):
    output = tmp_path / "report.md"
    output.write_bytes(b"previous complete\n")
    with pytest.raises(LimitExceededError):
        publish_report(run([], []), config(limits={"max_report_bytes": 1}), tmp_path, output, ())
    assert output.read_bytes() == b"previous complete\n"
