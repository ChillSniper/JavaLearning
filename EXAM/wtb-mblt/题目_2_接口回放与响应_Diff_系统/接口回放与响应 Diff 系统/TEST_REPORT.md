# 接口响应 Diff 系统测试记录

验证日期：2026-10-19。程序版本：1.0.0。

## 1. 执行环境

| 项目 | 实际环境 |
| --- | --- |
| 操作系统 | Windows 11，`Windows-11-10.0.26200-SP0` |
| Python | 项目 `.venv`，3.13.15 |
| PowerShell | 7.6.5 |
| CPU | `Intel64 Family 6 Model 186 Stepping 2, GenuineIntel`，20 个逻辑处理器 |
| 物理内存 | 16,961,822,720 bytes，约 15.80 GiB |
| 运行依赖 | `simplejson==3.20.2` |
| 主要测试依赖 | `pytest==9.1.1`、`pytest-cov==7.1.0`、`coverage==7.16.2`、`hypothesis==6.170.2`、`markdown-it-py==4.2.0`、`psutil==7.2.2` |

完整固定依赖见 [requirements.txt](requirements.txt) 和 [requirements-dev.txt](requirements-dev.txt)。实际执行 `python -m pip check`，结果为 `No broken requirements found.`。

全部测试命令在当前题目目录执行。`test.ps1` 将临时文件、子进程输入输出、日志和覆盖率数据保存在 `.cache/test-runs/<run_id>/`；该目录已经列入 `.gitignore`。下文的证据链接指向本次工作区保存的文件。

## 2. 五轮回归与最终完整回归

| 轮次 | 实际命令 | 结果 | 日志 |
| --- | --- | --- | --- |
| REG-01：规则验证 | `.\test.ps1 tests/unit -q` | 163 passed，0.75 秒 | [pytest.log](.cache/test-runs/20261019T135650-6756f16bd15b47438a34d48797758479/pytest.log) |
| REG-02：完整文件流程 | `.\test.ps1 tests/integration -q` | 11 passed，0.82 秒 | [pytest.log](.cache/test-runs/20261019T140325-c5d762c46f4b4d1b96926405aa002d20/pytest.log) |
| REG-03：命令行验证 | `.\test.ps1 tests/cli -q` | 9 passed，6.55 秒 | [pytest.log](.cache/test-runs/20261019T135650-1500093ec2814539abb6165bdd7dc50e/pytest.log) |
| REG-04：性质验证 | `.\test.ps1 tests/properties -q --hypothesis-seed=20261019 --hypothesis-show-statistics` | 9 passed，16.66 秒；每项 200 组通过输入 | [pytest.log](.cache/test-runs/20261019T135708-8bff086579434b189dbaaf171f18a6cc/pytest.log) |
| REG-05：容量验证 | `.\test.ps1 tests/performance -q -s` | 8 passed，16.91 秒；24 次独立子进程运行 | [pytest.log](.cache/test-runs/20261019T135754-b42bed5f96194eba8bf6d4cddc6087f3/pytest.log) |
| 最终完整回归 | `.\test.ps1 -q --hypothesis-seed=20261019` | **200 passed，64.52 秒，退出码 0** | [pytest.log](.cache/test-runs/20261019T140337-4b89be8b37b24ed09011e05d48e8d2ab/pytest.log) |

最终完整回归覆盖当前全部代码，包含报告元数据控制字符的处理。上表各专项数量相加为 200；参数化用例按 pytest 收集后的数量计算。

测试直接执行比较组件、JSON 文件读写、报告写入和 Python／PowerShell 子进程。原始资源的逐项预期保存在 [resource_default.json](tests/expected/resource_default.json)，完整报告预期保存在 [resource_default_report.md](tests/expected/resource_default_report.md)，测试执行时读取固定预期进行比较。

## 3. 设计用例与测试文件

`TechDesign.md` 的 95 个行为用例通过参数化单元测试、文件集成测试和 CLI 测试验证；9 项性质测试另外执行。

| 设计编号 | 数量 | 主要测试文件与检查内容 |
| --- | --- | --- |
| RES-01～RES-11 | 11 | `tests/integration/test_resources.py`：默认资源逐项事件、分类统计、相同记录、忽略命中、配置变化、重复运行、输入 SHA-256 |
| DIF-01～DIF-17 | 17 | `tests/unit/test_differ.py`：六类 JSON 类型的 30 个不同类型组合、精确 number、缺失与 null、根节点、父级容器、特殊字段路径、输入保护 |
| CFG-01～CFG-15 | 15 | `tests/unit/test_config_ignore.py`：读取实际配置文件、通配符、递归忽略、完整容器展示、非法配置、数组路径规则重叠、身份字段校验 |
| ARR-01～ARR-18 | 18 | `tests/unit/test_arrays.py`：ordered、unordered、match_key、重复次数、类型保留、新旧索引、嵌套规则、全部数组预检查 |
| CAN-01～CAN-10 | 10 | `tests/unit/test_candidates.py`、候选 JSON 文件集成测试：样本分母、精确请求分组、完整配对、缺失和类型变化、开关配置 |
| IO-01～IO-13 | 13 | `tests/unit/test_loader.py`、`tests/integration/test_report.py`、`tests/cli/test_cli.py`：严格 JSON、重复字段与 id、Unicode、输入身份、资源限制、实际文件错误、输入文件别名保护 |
| RPT-01～RPT-04 | 4 | `tests/integration/test_report.py`：Markdown parser 结构校验、完整长值、控制字符、比较对象、完整报告 bytes |
| CLI-01～CLI-07 | 7 | `tests/cli/test_cli.py`：实际入口、退出码 0／1／2／3、中文及空格路径、其他工作目录、参数传递 |

另有全局差异数量限制、报告大小边界、测试脚本自身执行和容量用例。报告验证使用 `markdown-it-py` 解析实际生成内容，检查表格列数、数据转义和节点类型；文件别名使用实际文件系统链接验证；写入失败使用实际目录作为输出目标验证。

## 4. 默认资源验收

实际执行 `.\run.ps1` 成功，退出码 0，生成 [DIFF_REPORT.md](DIFF_REPORT.md)。报告 bytes 与独立保存的完整预期相同。

| 检查项 | 实际结果 |
| --- | --- |
| 总记录数／有差异数／无差异数 | 7／4／3 |
| 差异总条数 | 10 |
| 状态码变更／字段删除／字段新增／字段类型变更／字段值变更 | 1／4／3／2／0 |
| 有差异记录 | `req_001`：3；`req_002`：3；`req_003`：3；`req_004`：1 |
| 无差异记录 | `req_005`、`req_006`、`req_007` |
| 旧版／新版忽略命中次数 | 23／23 |
| 疑似动态字段提示数量 | 0；当前精确请求分组未满足 3 条共同记录的样本条件 |
| 空忽略列表 | 7 条有差异记录，33 项差异 |
| 默认忽略列表增加 `*_at` | 4 条有差异记录，8 项差异 |
| old 与自身比较 | 7 条无差异记录，0 项差异 |
| 固定输入连续运行三次 | 报告 bytes 与 SHA-256 相同 |

SHA-256 核验值：

| 对象 | SHA-256 |
| --- | --- |
| `resources/old_responses.json` | `736c01d5c26bb4a6aa2e641a3397676823760211c7eebbbba519bfb3bfe008f3` |
| `resources/new_responses.json` | `3ab810cab06b76fcdf18dd3c3401c2b04804b6d88284f5ba730bf2af10dea3de` |
| `PROBLEM.md` | `e9ee04ab353feb91d949d07bccaa4335f9590504c21e01e811d11e93f0578fc6` |
| 默认有效配置 | `b3d9767469d92d1d0cc5c8231123836eff8f465e8a6d3cbb619ddd14f7a9d163` |
| `DIFF_REPORT.md` 与完整报告预期 | `f332581109f79cf8df0e05fac621308437dd92e446503d695190ff7697036d9b` |

输入保护同时通过文件执行前后 SHA-256 和内存对象执行前后内容检查验证。

## 5. 性质测试

固定种子为 `20261019`。以下每项获得 200 组通过输入，共 1,800 组；Hypothesis 因生成条件不满足而重新生成的输入不计入这个数量。详细统计见 REG-04 日志。

1. `test_reflexivity`：任意合法 JSON 与自身比较没有差异。
2. `test_direction_symmetry`：交换新旧输入时，新增与删除、旧值与新值具有对应关系。
3. `test_statistics_conservation`：记录并集、差异记录与相同记录的统计关系成立。
4. `test_ignore_invariance`：只改变被忽略字段时，比较结果保持一致。
5. `test_object_order_invariance`：object key 插入顺序不影响比较结论。
6. `test_unordered_permutation_and_counts`：无序数组重排不产生差异，重复次数变化能够识别。
7. `test_identity_movement`：身份字段配对能够处理元素移动，并保留字段变化。
8. `test_type_preservation`：string、number、boolean 类型保持独立。
9. `test_input_protection`：比较操作保持原始输入对象内容。

## 6. 覆盖率

最终完整回归的 [coverage.json](.cache/test-runs/20261019T140337-4b89be8b37b24ed09011e05d48e8d2ab/coverage.json) 记录：

| 指标 | 实际结果 |
| --- | --- |
| 语句覆盖 | 678／708，95.76% |
| 分支覆盖 | 257／260，98.85% |
| coverage 综合覆盖 | 96.59%，终端按整数显示为 97% |

`arrays.py`、`candidates.py`、`config.py`、`differ.py`、`ignore.py`、`jsonio.py`、`loader.py` 七个核心模块的语句和分支覆盖率均为 100%。`runner.py`、`models.py`、`paths.py` 的语句和分支覆盖率也为 100%。

当前覆盖率采集 pytest 所在进程。CLI 行为通过独立子进程实际执行，子进程中的 `__main__.py` 数据没有合并到此覆盖率文件。`report.py` 中跨文件系统输出的拒绝分支尚未在实际跨文件系统设备执行；同文件系统写入、完整替换、输入别名保护和实际写入失败均已测试。

## 7. 容量测量

以下采用最终完整回归保存的 24 份 `measurement.json`。每个场景由独立 Python 子进程重复 3 次。每次均检查差异数量、完整报告存在、执行时间小于 10 秒、进程峰值内存小于 512 MiB。

| 输入规模 | 数组模式 | 时间中位数（秒） | 三次最大时间（秒） | 三次最大峰值内存（MiB） | 每次差异数 |
| --- | --- | --- | --- | --- | --- |
| 1,000 条记录 | ordered | 0.1029 | 0.1161 | 47.91 | 667 |
| 10,000 条记录 | ordered | 0.5260 | 0.5448 | 77.94 | 6,667 |
| 1,000 个数组元素 | ordered | 0.1040 | 0.1099 | 45.48 | 2,000 |
| 1,000 个数组元素 | unordered | 0.0702 | 0.0841 | 45.37 | 2 |
| 1,000 个数组元素 | unordered + match_key | 0.0731 | 0.0768 | 45.45 | 1 |
| 10,000 个数组元素 | ordered | 0.5492 | 0.5638 | 58.85 | 20,000 |
| 10,000 个数组元素 | unordered | 0.2770 | 0.2838 | 60.32 | 2 |
| 10,000 个数组元素 | unordered + match_key | 0.2621 | 0.2760 | 52.34 | 1 |

记录场景按独立规则选择值变化、类型变化和相同记录，并加入配置忽略的字段。数组场景反转元素顺序，同时修改身份为 0 的元素内容。不同模式依据各自规则产生上表差异数量。

计时从实际输入文件写入完成后开始，覆盖读取、JSON 解析、校验、忽略处理、比较、候选分析、Markdown 生成及报告完整写入，包括 `fsync`；不包含输入构造和 Python 启动时间。Windows 峰值内存通过 `psutil.Process().memory_info().peak_wset` 读取，表示整个子进程的峰值 working set，包含解释器、依赖和输入构造期间的内存。

数据保存在最终证据目录的 `pytest/test_capacity_*/repeat-*/`，每次包含 `old.json`、`new.json`、`report.md` 和 `measurement.json`。这些测量对应本机离线快照比较流程。

## 8. 验证范围

Python 3.13.15、Windows 11 和 PowerShell 7.6.5 已执行完整回归。29 个 Python 文件通过 Python 3.11 语法规则检查；Python 3.11 运行环境及 Linux 环境尚未实际执行。

深度、节点数、数组长度、记录数量、输入大小、差异数量和报告大小的配置限制均有边界测试。极深输入按配置深度立即终止；parser 自身深度极限取决于具体 Python 和 simplejson 环境。

当前回放输入为已保存的响应快照，验收内容包含离线读取与比较流程。实际 HTTP 请求执行、并行写入同一个报告路径、超出配置限制的数据规模均属于本次测量范围之外。

## 9. 重复执行

```powershell
.\run.ps1
.\test.ps1 -q --hypothesis-seed=20261019
```

第一条命令重新生成默认报告，第二条命令执行当前全部 200 项测试并创建独立证据目录。需要查看每项性质的输入数量时执行 REG-04 所列命令。算法、配置及入口说明见 [README.md](README.md)，完整设计见 [TechDesign.md](TechDesign.md)。
