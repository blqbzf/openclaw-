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
    '--onefile',
    '--add-data', f'{ROOT / "launcher_config.json"}{SEPARATOR}.',
    '--add-data', f'{ROOT / "assets"}{SEPARATOR}assets',
    str(ROOT / 'wow_launcher.py'),
]

subprocess.run(cmd, check=True)

single_exe = DIST / f'{APP_NAME}.exe'
portable_dir = DIST / APP_NAME
portable_dir.mkdir(parents=True, exist_ok=True)

if single_exe.exists():
    shutil.copy2(single_exe, portable_dir / single_exe.name)

for extra in ['launcher_config.json', 'README.md']:
    src = ROOT / extra
    if src.exists():
        shutil.copy2(src, portable_dir / extra)

assets_src = ROOT / 'assets'
assets_dst = portable_dir / 'assets'
if assets_src.exists():
    if assets_dst.exists():
        shutil.rmtree(assets_dst)
    shutil.copytree(assets_src, assets_dst)

print(f'Build complete: {single_exe}')
print(f'Portable dir: {portable_dir}')
