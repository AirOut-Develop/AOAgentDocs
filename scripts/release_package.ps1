# release_package.ps1 - AOAgentDocs 릴리즈 패키징 스크립트 (Windows Native)
# 사용법: pwsh -File scripts/release_package.ps1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$VersionFile = Join-Path $RootDir "VERSION"

if (-not (Test-Path $VersionFile)) {
    Write-Error "VERSION 파일이 없습니다: $VersionFile"
    exit 1
}

$Version = (Get-Content $VersionFile -Raw).Trim()
if ([string]::IsNullOrWhiteSpace($Version)) {
    Write-Error "VERSION 값이 비어 있습니다."
    exit 1
}

$DistDir = Join-Path $RootDir "dist"
$OutFile = Join-Path $DistDir "AOAgentDocs_v${Version}.zip"

if (-not (Test-Path $DistDir)) {
    New-Item -ItemType Directory -Path $DistDir -Force | Out-Null
}

# 제외할 패턴
$ExcludeNames = @(".git", "dist", ".idea", ".omc", ".codex", ".vscode")

# 임시 폴더 생성
$TmpDir = Join-Path ([System.IO.Path]::GetTempPath()) "AOAgentDocs_release_$(Get-Random)"
$PkgDir = Join-Path $TmpDir "AOAgentDocs"
New-Item -ItemType Directory -Path $PkgDir -Force | Out-Null

try {
    # 파일 복사 (제외 목록 적용)
    Get-ChildItem -Path $RootDir -Force | Where-Object {
        $ExcludeNames -notcontains $_.Name
    } | ForEach-Object {
        if ($_.PSIsContainer) {
            Copy-Item -Path $_.FullName -Destination (Join-Path $PkgDir $_.Name) -Recurse -Force
        } else {
            Copy-Item -Path $_.FullName -Destination $PkgDir -Force
        }
    }

    # 기존 zip 삭제 후 생성
    if (Test-Path $OutFile) {
        Remove-Item $OutFile -Force
    }

    Compress-Archive -Path "$PkgDir\*" -DestinationPath $OutFile -Force
    Write-Host "릴리즈 패키지 생성 완료: $OutFile"
}
finally {
    # 임시 폴더 정리
    if (Test-Path $TmpDir) {
        Remove-Item $TmpDir -Recurse -Force
    }
}
