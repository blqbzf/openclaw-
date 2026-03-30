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
$VcpkgRoot = Join-Path $Root 'tools/vcpkg'
$VcpkgExe = Join-Path $VcpkgRoot 'vcpkg.exe'
$VcpkgToolchain = Join-Path $VcpkgRoot 'scripts/buildsystems/vcpkg.cmake'
$SmpqExe = Join-Path $SmpqBuild 'Release/smpq.exe'

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

if (!(Test-Path $SmpqExe)) {
  if (!(Test-Path $SmpqRoot)) { git clone --depth 1 https://github.com/bubio/smpq $SmpqRoot }
  if (!(Test-Path $VcpkgRoot)) { git clone --depth 1 https://github.com/microsoft/vcpkg $VcpkgRoot }
  if (!(Test-Path $VcpkgExe)) { & (Join-Path $VcpkgRoot 'bootstrap-vcpkg.bat') -disableMetrics }
  if (!(Test-Path $VcpkgExe)) { throw 'vcpkg bootstrap failed' }

  & $VcpkgExe install stormlib:x64-windows
  if ($LASTEXITCODE -ne 0) { throw 'vcpkg stormlib install failed' }

  cmake -S $SmpqRoot -B $SmpqBuild -A x64 -DWITH_KDE=OFF "-DCMAKE_TOOLCHAIN_FILE=$VcpkgToolchain"
  if ($LASTEXITCODE -ne 0) { throw 'smpq cmake configure failed' }

  cmake --build $SmpqBuild --config Release --target smpq
  if ($LASTEXITCODE -ne 0) { throw 'smpq build failed' }
}

if (!(Test-Path $SmpqExe)) {
  $altExe = Join-Path $SmpqBuild 'smpq.exe'
  if (Test-Path $altExe) { $SmpqExe = $altExe }
}
if (!(Test-Path $SmpqExe)) { throw "smpq build failed: $SmpqExe missing" }
if (Test-Path $OutputMpq) { Remove-Item $OutputMpq -Force }

Push-Location $StagePath
& $SmpqExe create $OutputMpq
if ($LASTEXITCODE -ne 0) { throw 'smpq create failed' }
Get-ChildItem -Recurse -File | ForEach-Object {
  $localFile = $_.FullName
  $relative = $localFile.Substring($StagePath.Length + 1).Replace('/', '\\')
  & $SmpqExe add $OutputMpq $relative $localFile
  if ($LASTEXITCODE -ne 0) { throw "smpq add failed for $relative" }
}
Pop-Location

Write-Host "[done ] MPQ => $OutputMpq"
