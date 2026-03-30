param(
  [string]$IconName = "INV_Misc_Book_WuZiTianShu"
)

$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
$SrcPng = Join-Path $Root "assets/icons-src/$IconName.png"
$BuildRoot = Join-Path $Root "build/patch-work"
$IconsDir = Join-Path $BuildRoot "Interface/Icons"
$OutDir = Join-Path $Root "dist"
$BlpPath = Join-Path $IconsDir "$IconName.blp"
$MpqPath = Join-Path $OutDir "Patch-WuZiTianShu.mpq"

New-Item -ItemType Directory -Force -Path $IconsDir | Out-Null
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
Copy-Item $SrcPng (Join-Path $IconsDir "$IconName.png") -Force

$Cli = Join-Path $Root 'tools/BlpCli/bin/Release/net9.0/BlpCli.exe'
if (!(Test-Path $Cli)) { throw "BlpCli not found: $Cli" }
& $Cli $SrcPng $BlpPath dxt5 0
if ($LASTEXITCODE -ne 0) { throw "BlpCli failed with code $LASTEXITCODE" }
Write-Host "[done ] PNG -> BLP => $BlpPath"
Write-Host "[todo ] pack MPQ => $MpqPath"

"ICON_NAME=$IconName" | Out-File -FilePath (Join-Path $OutDir "patch.env") -Encoding utf8
"PNG_PATH=$SrcPng" | Add-Content -Path (Join-Path $OutDir "patch.env")
"BLP_PATH=$BlpPath" | Add-Content -Path (Join-Path $OutDir "patch.env")
"MPQ_PATH=$MpqPath" | Add-Content -Path (Join-Path $OutDir "patch.env")
