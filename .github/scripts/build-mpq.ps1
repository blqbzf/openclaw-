param(
  [string]$PatchName = "Patch-WuZiTianShu.mpq",
  [string]$StageDir = "patches/src/wuzitianshu",
  [string]$OutDir = "patches/dist"
)

$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
$StagePath = Join-Path $Root $StageDir
$OutputDir = Join-Path $Root $OutDir
$OutputMpq = Join-Path $OutputDir $PatchName
$SmpqRoot = Join-Path $Root 'tools/smpq'
$SmpqBuild = Join-Path $SmpqRoot 'build'
$SmpqExe = Join-Path $SmpqBuild 'Release/smpq.exe'

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

if (!(Test-Path $SmpqExe)) {
  git clone --depth 1 https://github.com/bubio/smpq $SmpqRoot
  cmake -S $SmpqRoot -B $SmpqBuild -A x64
  cmake --build $SmpqBuild --config Release
}

if (!(Test-Path $SmpqExe)) { throw "smpq build failed: $SmpqExe missing" }
if (Test-Path $OutputMpq) { Remove-Item $OutputMpq -Force }

Push-Location $StagePath
& $SmpqExe create $OutputMpq
Get-ChildItem -Recurse -File | ForEach-Object {
  $localFile = $_.FullName
  $relative = $localFile.Substring($StagePath.Length + 1).Replace('/', '\\')
  & $SmpqExe add $OutputMpq $relative $localFile
  if ($LASTEXITCODE -ne 0) { throw "smpq add failed for $relative" }
}
Pop-Location

Write-Host "[done ] MPQ => $OutputMpq"
