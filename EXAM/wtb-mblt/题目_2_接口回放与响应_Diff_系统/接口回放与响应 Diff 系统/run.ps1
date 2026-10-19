[CmdletBinding(PositionalBinding = $false)]
param(
    [string]$Python = (Join-Path $PSScriptRoot '.venv/Scripts/python.exe'),
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$DiffArguments
)

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    throw '缺少 Python 环境，请执行 py -3.13 -m venv .venv 并安装 requirements.txt。'
}
& $Python -c 'import sys, importlib.util; assert sys.version_info >= (3, 11), "需要 Python 3.11 及以上"; assert importlib.util.find_spec("simplejson"), "请执行当前 Python 的 -m pip install -r requirements.txt 命令"'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Push-Location -LiteralPath $PSScriptRoot
try {
    & $Python -m response_diff @DiffArguments
    $DiffExitCode = $LASTEXITCODE
}
finally {
    Pop-Location
}
exit $DiffExitCode
