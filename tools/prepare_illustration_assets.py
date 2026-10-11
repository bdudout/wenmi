"""Copy generated originals and encode web assets. Usage: script slug source.png ..."""
from pathlib import Path
import json
import shutil
import sys
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ORIGINALS = ROOT.parent / 'wenmi' / 'illustrations'
DEST = ROOT / 'assets' / 'img' / 'illustrations'
DEST.mkdir(parents=True, exist_ok=True)
manifest_path = DEST / 'manifest.json'
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
for slug, source in zip(sys.argv[1::2], sys.argv[2::2]):
    original = ORIGINALS / f'{slug}.png'
    output = DEST / f'{slug}.webp'
    if original.exists() or output.exists():
        raise FileExistsError(f'Refusing to overwrite {slug}')
    shutil.copy2(source, original)
    with Image.open(original) as im:
        im = im.convert('RGB')
        im.thumbnail((1600, 1200), Image.Resampling.LANCZOS)
        im.save(output, 'WEBP', quality=85, method=6)
        manifest[slug] = {'width': im.width, 'height': im.height, 'bytes': output.stat().st_size,
                          'original': f'wenmi/illustrations/{slug}.png'}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(manifest, ensure_ascii=False, indent=2))
