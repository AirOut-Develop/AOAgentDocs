# Python 3.10+; identical payload builder on Windows/Linux/macOS.
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 (Join-Path $RootDir "scripts/release_package.py")
} else {
    & python (Join-Path $RootDir "scripts/release_package.py")
}
exit $LASTEXITCODE
