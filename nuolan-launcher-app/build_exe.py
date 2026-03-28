from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
BUILD = ROOT / 'build'
APP_NAME = 'NuolanWoWLauncher'
SEPARATOR = ';' if sys.platform.startswith('win') else ':'

for p in [DIST, BUILD]:
    if p.exists():
        shutil.rmtree(p)

cmd = [
    sys.executable,
    '-m', 'PyInstaller',
    '--noconfirm',
    '--clean',
    '--windowed',
    '--name', APP_NAME,
    '--onedir',
    '--add-data', f'{ROOT / "launcher_config.json"}{SEPARATOR}.',
    '--add-data', f'{ROOT / "assets"}{SEPARATOR}assets',
    str(ROOT / 'wow_launcher.py'),
]

subprocess.run(cmd, check=True)

bundle_dir = DIST / APP_NAME
for extra in ['launcher_config.json', 'README.md']:
    src = ROOT / extra
    if src.exists():
        shutil.copy2(src, bundle_dir / extra)

assets_src = ROOT / 'assets'
assets_dst = bundle_dir / 'assets'
if assets_src.exists() and not assets_dst.exists():
    shutil.copytree(assets_src, assets_dst)

print(f'Build complete: {bundle_dir}')
