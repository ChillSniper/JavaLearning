[CmdletBinding(PositionalBinding = $false)]
param(
    [string]$Python = (Join-Path $PSScriptRoot '.venv/Scripts/python.exe'),
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$TestArguments
)

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
$RunId = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmss') + '-' + [Guid]::NewGuid().ToString('N')
$RunDirectory = Join-Path $PSScriptRoot ('.cache/test-runs/' + $RunId)
New-Item -ItemType Directory -Path $RunDirectory -Force | Out-Null
$PreviousEnvironment = @{}
foreach ($Name in @('TMP', 'TEMP', 'TMPDIR', 'COVERAGE_FILE', 'PYTHONUTF8')) {
    $PreviousEnvironment[$Name] = [Environment]::GetEnvironmentVariable($Name, 'Process')
}
foreach ($Name in @('TMP', 'TEMP', 'TMPDIR')) {
    [Environment]::SetEnvironmentVariable($Name, $RunDirectory, 'Process')
}
$env:COVERAGE_FILE = Join-Path $RunDirectory 'coverage'
$env:PYTHONUTF8 = '1'
Push-Location -LiteralPath $PSScriptRoot
try {
    & $Python -m pytest --basetemp (Join-Path $RunDirectory 'pytest') --cov=response_diff --cov-branch --cov-report=term-missing --cov-report="json:$RunDirectory/coverage.json" @TestArguments 2>&1 | Tee-Object -FilePath (Join-Path $RunDirectory 'pytest.log')
    $TestExitCode = $LASTEXITCODE
    Write-Output ('测试证据：' + $RunDirectory)
}
finally {
    Pop-Location
    foreach ($Name in $PreviousEnvironment.Keys) {
        [Environment]::SetEnvironmentVariable($Name, $PreviousEnvironment[$Name], 'Process')
    }
}
exit $TestExitCode
