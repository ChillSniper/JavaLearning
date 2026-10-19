import argparse
from pathlib import Path

from .config import load_config
from .report import MarkdownRenderer, ReportWriter
from .runner import SnapshotReplayRunner

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def project_path(value: str) -> Path:
    path = Path(value)
    return (PROJECT_ROOT / path).resolve() if not path.is_absolute() else path.resolve()


def main() -> int:
    parser = argparse.ArgumentParser(description="接口响应快照回放与字段比较")
    parser.add_argument("--old", default="resources/old_responses.json", help="旧版 JSON，路径相对于项目目录")
    parser.add_argument("--new", default="resources/new_responses.json", help="新版 JSON，路径相对于项目目录")
    parser.add_argument("--config", default="config.json", help="JSON 配置文件")
    parser.add_argument("--output", default="DIFF_REPORT.md", help="Markdown 输出文件")
    parser.add_argument("--fail-on-diff", action="store_true", help="报告存在差异时返回 3")
    args = parser.parse_args()
    old, new, config_path = (project_path(value) for value in (args.old, args.new, args.config))
    writer = ReportWriter(PROJECT_ROOT)
    output = writer.prepare(project_path(args.output), (old, new, config_path))
    config = load_config(config_path)
    result = SnapshotReplayRunner(config).run_files(old, new)
    content = MarkdownRenderer().render(result, config.limits.max_report_bytes)
    writer.write(output, content)
    print(f"总记录数：{result.total}，有差异数：{result.changed}，无差异数：{result.unchanged}，差异明细：{result.diff_count}")
    print(f"报告：{output}")
    return 3 if args.fail_on_diff and result.changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
