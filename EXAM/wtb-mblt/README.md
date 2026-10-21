# 你的 vibecoding 面试工作区

## 题目
join 不会自动下载题面/起始代码。看 `.vibecoding/problems.json` 里列出你能做的题，
然后用 `vc download <problemName>` 把指定题目的文件拉到本地。

## 写代码
在 `<problemName>/` 目录下编辑题目代码。
考试进行中时，`vc status` 会在后台静默同步代码到服务端。
也可手动：`vc upload <problemName>` / `vc submit <problemName>`。

推荐工具:
- VSCode:       code .
- Cursor:       cursor .
- Claude Code:  在本目录直接跑 `claude`
- opencode:     在本目录直接跑 `opencode`

## 注意
- .vibecoding/ 目录是 CLI 内部用的，别动
