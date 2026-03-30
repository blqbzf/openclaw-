param(
  [string]$PatchName = "patch-Z.mpq",
  [string]$LocalePatchName = "patch-zhCN-Z.mpq",
  [string]$StageDir = "patches/src/wuzitianshu",
  [string]$OutDir = "patches/dist"
)

$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
$StagePath = Join-Path $Root $StageDir
$OutputDir = Join-Path $Root $OutDir
$OutputMpq = Join-Path $OutputDir $PatchName
$LocaleOutputMpq = Join-Path $OutputDir $LocalePatchName
$MpqCliRoot = Join-Path $Root 'tools/mpqcli'
$MpqCliBuild = Join-Path $MpqCliRoot 'build'
$MpqCliExe = Join-Path $MpqCliBuild 'Release/mpqcli.exe'
$MpqCliExeBin = Join-Path $MpqCliBuild 'bin/Release/mpqcli.exe'

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

if (!(Test-Path $MpqCliExe)) {
  if (!(Test-Path $MpqCliRoot)) { git clone --depth 1 --recurse-submodules https://github.com/TheGrayDot/mpqcli $MpqCliRoot }

  Push-Location $MpqCliRoot
  git submodule update --init --recursive
  if ($LASTEXITCODE -ne 0) { throw 'mpqcli submodule init failed' }
  Pop-Location

  cmake -S $MpqCliRoot -B $MpqCliBuild -A x64
  if ($LASTEXITCODE -ne 0) { throw 'mpqcli cmake configure failed' }

  cmake --build $MpqCliBuild --config Release
  if ($LASTEXITCODE -ne 0) { throw 'mpqcli build failed' }
}

if (!(Test-Path $MpqCliExe)) {
  if (Test-Path $MpqCliExeBin) { $MpqCliExe = $MpqCliExeBin }
  else {
    $altExe = Join-Path $MpqCliBuild 'mpqcli.exe'
    if (Test-Path $altExe) { $MpqCliExe = $altExe }
  }
}
if (!(Test-Path $MpqCliExe)) { throw "mpqcli build failed: $MpqCliExe missing" }
if (Test-Path $OutputMpq) { Remove-Item $OutputMpq -Force }
if (Test-Path $LocaleOutputMpq) { Remove-Item $LocaleOutputMpq -Force }

& $MpqCliExe create $StagePath -o $OutputMpq
if ($LASTEXITCODE -ne 0) { throw 'mpqcli create failed' }

Copy-Item $OutputMpq $LocaleOutputMpq -Force

Write-Host "[done ] MPQ => $OutputMpq"
Write-Host "[done ] Locale MPQ => $LocaleOutputMpq"
