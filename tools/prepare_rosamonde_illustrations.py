"""Preserve PNG originals and encode WebP assets without overwriting existing files."""
import json
from pathlib import Path
import shutil
import sys
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ORIGINALS = ROOT.parent / 'wenmi/illustrations/rosamonde'
DEST = ROOT / 'assets/img/rosamonde/illustrations'


def prepare(args):
    if not args or len(args) % 2:
        raise SystemExit('Usage: prepare_rosamonde_illustrations.py slug source.png ...')
    ORIGINALS.mkdir(parents=True, exist_ok=True)
    DEST.mkdir(parents=True, exist_ok=True)
    manifest_path = DEST / 'manifest.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    for slug, source in zip(args[::2], args[1::2]):
        if Path(slug).name != slug:
            raise ValueError('Slug must be a basename')
        original = ORIGINALS / f'{slug}.png'
        output = DEST / f'{slug}.webp'
        if original.exists() or output.exists():
            raise FileExistsError(f'Refusing to overwrite {slug}')
        shutil.copy2(source, original)
        with Image.open(original) as image:
            image = image.convert('RGB')
            image.thumbnail((1600, 1200), Image.Resampling.LANCZOS)
            image.save(output, 'WEBP', quality=85, method=6)
            manifest[slug] = dict(width=image.width, height=image.height,
                                  bytes=output.stat().st_size,
                                  original=f'wenmi/illustrations/rosamonde/{slug}.png')
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
        print(f'{slug}: {manifest[slug]["bytes"]} bytes')


if __name__ == '__main__':
    prepare(sys.argv[1:])
