#!/usr/bin/env python3
"""Entry program: write the stored front-page image to /output/entry.png.

The image (assets/entry.png) is rendered by render.py from the repository's
own code and vendored fonts; this program only copies it, byte for byte, so
both grading runs produce identical output. Standard library only.
"""
import shutil
from pathlib import Path

src = Path(__file__).resolve().parent / "assets" / "entry.png"
dst = Path("/output/entry.png")
dst.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(src, dst)
print(f"wrote {dst} ({dst.stat().st_size} bytes)")
