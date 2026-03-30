from __future__ import annotations
import hashlib, json, os
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
PATCH_DIR = ROOT / 'patches' / 'dist'
MANIFEST_PATH = ROOT / 'patch-manifests' / 'manifest.json'
VERSION_PATH = ROOT / 'patch-manifests' / 'version.json'
BASE_DOWNLOAD = 'https://github.com/blqbzf/openclaw-/releases/download/patches-latest'

patches = []
for file in sorted(PATCH_DIR.glob('*.mpq')):
    data = file.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    relative_path = f'Data/{file.name}'
    lower_name = file.name.lower()
    if lower_name.startswith('patch-zhcn-'):
        relative_path = f'Data/zhCN/{file.name}'

    patches.append({
        'Name': file.stem,
        'Version': datetime.now(timezone.utc).strftime('%Y.%m.%d.%H%M'),
        'Size': len(data),
        'Sha256': sha,
        'DownloadUrl': f'{BASE_DOWNLOAD}/{file.name}',
        'LocalRelativePath': relative_path,
        'Required': True,
    })

MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
MANIFEST_PATH.write_text(json.dumps(patches, ensure_ascii=False, indent=2), encoding='utf-8')
VERSION_PATH.write_text(json.dumps({
    'generatedAt': datetime.now(timezone.utc).isoformat(),
    'patchCount': len(patches),
    'channel': 'patches-latest'
}, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'generated manifest patches={len(patches)}')
