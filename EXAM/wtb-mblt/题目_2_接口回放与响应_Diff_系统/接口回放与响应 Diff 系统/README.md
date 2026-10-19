# 接口回放与响应 Diff 系统

## 环境准备

需要 Python 3.11 及以上。当前完整回归环境为 Windows 11、Python 3.13.15、PowerShell 7。以下命令在当前题目目录执行：

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

`requirements.txt` 固定运行依赖；`requirements-dev.txt` 另外固定测试、覆盖率、性质测试、Markdown 校验和进程内存测量所需依赖。仅运行工具时可安装 `requirements.txt`。

## 一键运行

```powershell
.\run.ps1
```

默认读取当前项目的 `resources/old_responses.json`、`resources/new_responses.json` 和 `config.json`，生成 `DIFF_REPORT.md`。`run.ps1` 使用项目内 `.venv`，也可以通过 `-Python` 指定 Python 可执行文件。

```powershell
.\.venv\Scripts\python.exe -m response_diff
```

默认资源的实际结果：7 条记录、4 条存在差异、3 条没有差异，共 10 项差异。

```powershell
.\run.ps1 --old resources/old_responses.json --new resources/new_responses.json --config config.json --output DIFF_REPORT.md --fail-on-diff
```

所有相对参数路径均相对于项目目录解释。PowerShell 脚本可从其他工作目录调用。

| 退出码 | 说明 |
| --- | --- |
| 0 | 完整报告已经生成，默认允许存在差异 |
| 3 | 使用 `--fail-on-diff` 且报告存在差异 |
| 2 | 命令行参数无效 |
| 1 | 读取、数据、配置、比较或写入发生异常 |

## 数据文件与记录配对

| 文件 | 说明 |
| --- | --- |
| `resources/old_responses.json` | 旧版响应快照，作为比较基准，包含 7 条记录 |
| `resources/new_responses.json` | 新版响应快照，包含 7 条记录 |

文件均为 JSON 数组。每条记录包含 `id`、`description`、`request.method`、`request.path`、`response.status`、`response.body`。body 支持全部六类 JSON 值。

记录按 `id` 配对，总数量使用两个 id 集合的并集大小。记录新增、删除分别报告。相同 id 的 method、path 必须一致，重复 id 或 JSON 字段名立即报错。输入文件与原始对象保持原始内容。

回放使用已采集的响应快照。请求 method、path 用于记录身份和报告展示；当前输入流程执行离线比较。

## Diff 算法

比较引擎使用明确的 JSON 类型和递归规则：

1. 字段只有一侧存在时，报告字段新增或删除，并保存完整内容。
2. 两侧类型不同，报告当前字段的类型变化。
3. 两侧均为 object，按字段名称并集递归比较；均为 array，使用路径对应的数组规则。
4. 同类型标量按精确值比较；HTTP status 单独比较。

JSON number 使用 `int`、`Decimal` 精确表达。`"128" → 128`、`true → 1` 均报告类型变化；`1 → 1.0` 具有相同 number 值。缺失与 null 分别表达。

父级新增、删除或类型变化在当前路径产生一条差异；报告包含该节点的完整内容。普通对象路径展示为 `data.author_email`，数组展示为 `data.items[0].name`，特殊字段名称通过 JSON 字符串形式展示。内部路径使用 typed segments。

## 配置格式

`ignore_fields` 为必填数组，允许空数组。默认配置包含题目指定的 `timestamp`、`traceId`、`request_id`、`created_at`。

```json
{
  "ignore_fields": ["timestamp", "traceId", "request_id", "created_at"],
  "arrays": {
    "default_mode": "ordered",
    "rules": [
      {"path": ["data", "tags"], "mode": "unordered"},
      {"path": ["data", "items"], "mode": "unordered", "match_key": ["id"]},
      {"path": ["data", "groups", null, "members"], "mode": "unordered", "match_key": ["user_id"]}
    ]
  },
  "dynamic_candidates": {"enabled": true, "min_samples": 3}
}
```

忽略模式匹配 body 中任意层级的字段名称，区分大小写，支持 `fnmatchcase` 的 `*`、`?`、`[seq]`、`[!seq]`。命中后移除该字段及其子节点，比较、数组匹配和报告值展示使用相同视图。HTTP status 与记录元数据保持各自处理规则。

默认不包含 `*_at`；用户加入该模式后，`updated_at` 也被忽略，当前资源结果为 8 项差异。空忽略列表对应 33 项差异。

数组配置的 `path` 相对于 body 根节点：string 表示 object key，非负 int 表示索引，null 表示任意数组索引，空数组表示 body 根节点。

| 模式 | 比较规则 |
| --- | --- |
| `ordered` | 按索引递归比较，长度差产生元素新增、删除 |
| `unordered` | 按包含类型的完整结构签名匹配，保留重复元素出现次数；不同元素产生新增、删除 |
| `unordered` 配合 `match_key` | 按显式身份字段匹配 object，再递归比较字段；报告保留旧、新索引 |

身份字段必须存在、非 null，类型为 string、number 或 boolean，并且在各自数组内部唯一。重复、缺失、被忽略规则覆盖的身份字段立即报错。unordered 内部路径使用 null 索引，重叠规则直接报错。

疑似动态字段按精确 method、path 和标准字段路径分组。默认至少需要 3 条共同记录；字段在每条记录中均存在、类型一致且全部变化时提供提示。数组中存在不完整配对时，该路径无法满足候选条件。提示保留全部正式差异，由人工确认是否修改配置。

`limits` 支持 `max_file_bytes`、`max_records`、`max_depth`、`max_nodes`、`max_array_items`、`max_diff_entries`、`max_report_bytes`。具体默认值见 `config.json`。配置未知字段、非正整数限制、非法模式均立即报错。

## 报告与文件行为

报告包含输入与有效配置 SHA-256、记录统计、差异分类、忽略命中次数、逐条明细、相同记录清单及候选提示。原始输入 bytes 与有效配置相同时，报告 bytes 相同。

Markdown 中的输入内容经过字符转义；JSON 数值及容器内容完整展示。报告使用 UTF-8、LF 和末尾换行。

报告通过 `.cache/report-staging/` 内的完整中间文件和 `os.replace` 发布。输出与输入、配置相同或位于其他文件系统时立即终止。发生异常时，本次运行没有成功结果，已有完整报告保持原始内容。每个输出路径由单个进程负责。

## 回归测试

```powershell
.\test.ps1
```

测试脚本将临时文件、日志、覆盖率数据保存到项目 `.cache/test-runs/<run_id>/`，并输出本次证据目录。

```powershell
.\test.ps1 tests/unit -q
.\test.ps1 tests/integration -q
.\test.ps1 tests/cli -q
.\test.ps1 tests/properties -q --hypothesis-seed=20261019 --hypothesis-show-statistics
.\test.ps1 tests/performance -q -s
```

测试直接执行实际组件、文件及 CLI 子进程。原始资源的逐项预期位于 `tests/expected/resource_default.json`，完整报告预期位于 `tests/expected/resource_default_report.md`。测试执行时读取固定预期。

9 项 Hypothesis 性质各执行 200 组输入。容量检查覆盖 1,000／10,000 条记录、1,000／10,000 个数组元素和三种数组模式，每组由独立子进程重复 3 次。

设计规则见 `TechDesign.md`；五轮实际回归结果、覆盖率、容量测量与验证范围见 `TEST_REPORT.md`。
