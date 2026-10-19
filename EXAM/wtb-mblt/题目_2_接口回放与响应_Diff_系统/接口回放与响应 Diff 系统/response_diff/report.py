import os
import tempfile
from pathlib import Path

from .config import DiffConfig
from .errors import InputValidationError, LimitExceededError
from .jsonio import dumps
from .models import DiffKind, RunResult
from .paths import diff_path, display_path

REPORT_VERSION = "1"


def escape_text(value: str) -> str:
    value = "".join(character.encode("unicode_escape").decode("ascii") if ord(character) < 32 else character for character in value)
    return "".join(
        f"&#{ord(character)};" if character in "&<>|\\`*_[]" else character
        for character in value
    )


def value_text(present: bool, kind: str | None, value: object) -> str:
    if not present:
        return "字段不存在"
    if kind == "null":
        return "null"
    return kind + " " + dumps(value)


def table(headers: tuple[str, ...], rows: list[tuple]) -> list[str]:
    return [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
        *("| " + " | ".join(escape_text(str(cell)) for cell in row) + " |" for row in rows),
        "",
    ]


class MarkdownRenderer:
    def render(self, result: RunResult, max_bytes: int) -> bytes:
        lines = [
            "# 接口响应 Diff 报告", "",
            f"报告格式版本：{REPORT_VERSION}", "",
            f"旧版输入 SHA-256：{result.old_sha256}", "",
            f"新版输入 SHA-256：{result.new_sha256}", "",
            f"有效配置 SHA-256：{result.config_sha256}", "",
            "## 记录统计", "",
        ]
        counts = result.counts
        added, removed = counts[DiffKind.RECORD_ADDED], counts[DiffKind.RECORD_REMOVED]
        lines.extend(table(
            ("总记录数", "有差异数", "无差异数", "共同记录数", "记录新增数", "记录删除数"),
            [(result.total, result.changed, result.unchanged, result.total - added - removed, added, removed)],
        ))
        lines += ["## 差异分类", ""]
        lines.extend(table(("Diff 类型", "条数"), [(kind.value, counts[kind]) for kind in DiffKind]))
        lines += [f"差异明细总条数：{result.diff_count}", "", "## 忽略处理统计", ""]
        lines.extend(table(("旧版命中数", "新版命中数"), [(result.ignored_old, result.ignored_new)]))
        lines += ["## 差异明细", ""]
        for record in result.records:
            if not record.diffs:
                continue
            title = f"{record.id} - {record.description}（{record.method} {record.request_path}）"
            lines += ["### " + escape_text(title), ""]
            if record.old_description is not None:
                lines += ["旧版描述：" + escape_text(record.old_description), ""]
            rows = [
                ({"status": "HTTP", "body": "body", "record": "record"}[diff.scope],
                 diff_path(diff), diff.kind.value,
                 value_text(diff.old_present, diff.old_type, diff.old_value),
                 value_text(diff.new_present, diff.new_type, diff.new_value))
                for diff in record.diffs
            ]
            lines.extend(table(("比较对象", "字段路径", "Diff 类型", "旧值", "新值"), rows))
        if not result.changed:
            lines += ["差异记录数量：0", ""]
        lines += ["## 无差异记录", ""]
        rows = [(record.id, record.description, record.method, record.request_path) for record in result.records if not record.diffs]
        lines.extend(table(("id", "请求描述", "method", "path"), rows))
        for record in result.records:
            if not record.diffs and record.old_description is not None:
                lines += [escape_text(record.id + " 旧版描述：" + record.old_description), ""]
        lines += ["## 疑似动态字段", "", f"提示数量：{len(result.candidates)}", ""]
        if result.candidates:
            lines.extend(table(
                ("method", "path", "字段路径", "变化样本数/样本数", "比例", "提示"),
                [(item.method, item.request_path, display_path(item.path), f"{item.changed}/{item.samples}", "100%", "疑似动态字段，需人工确认") for item in result.candidates],
            ))
        content = "\n".join(lines).encode("utf-8")
        if len(content) > max_bytes:
            raise LimitExceededError(f"超过 max_report_bytes={max_bytes}")
        return content


class ReportWriter:
    def __init__(self, project_root: Path):
        self.staging = project_root / ".cache" / "report-staging"

    def prepare(self, output: Path, protected: tuple[Path, ...]) -> Path:
        output = output.resolve()
        for source in protected:
            if output == source.resolve() or output.exists() and source.exists() and output.samefile(source):
                raise InputValidationError("输出路径与输入或配置文件相同")
        output.parent.mkdir(parents=True, exist_ok=True)
        self.staging.mkdir(parents=True, exist_ok=True)
        if output.parent.stat().st_dev != self.staging.stat().st_dev:
            raise InputValidationError("输出路径与报告中间目录必须位于同一文件系统")
        return output

    def write(self, output: Path, content: bytes) -> None:
        with tempfile.NamedTemporaryFile(dir=self.staging, suffix=".tmp", delete=False) as stream:
            temporary_path = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, output)


def publish_report(result: RunResult, config: DiffConfig, project_root: Path, output: Path, protected: tuple[Path, ...]) -> None:
    writer = ReportWriter(project_root)
    destination = writer.prepare(output, protected)
    writer.write(destination, MarkdownRenderer().render(result, config.limits.max_report_bytes))
