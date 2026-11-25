#!/usr/bin/env python3
"""Validate KMISynth patch files in Patches/.

Checks every file under Patches/:
  - lives in an allowed category folder (Patches/<Category>/<file>)
  - is a .kmip file (or .gitkeep)
  - has a valid file name and is under the size limit
  - is well-formed XML with a <KMISynth> root element and no DOCTYPE
  - has at least one tag
  - does not clash (case-insensitively) with another patch in the same folder

Exits 1 and prints a GitHub Actions error annotation for each problem found.
"""

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATCHES = ROOT / "Patches"
CATEGORIES = {
    "Arp", "Bass", "Bells", "Brass", "Drone", "FX", "Keys",
    "Lead", "Organ", "Pad", "Pluck", "Sequence",
}
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _'\-]{0,47}$")
MAX_BYTES = 5 * 1024 * 1024  # user wavetables are embedded, so allow some room

errors: list[str] = []


def fail(path: Path, msg: str) -> None:
    rel = path.relative_to(ROOT).as_posix()
    errors.append(f"{rel}: {msg}")
    print(f"::error file={rel}::{msg}")


def check_patch(path: Path) -> None:
    stem = path.stem
    if not NAME_RE.match(stem):
        fail(path, "file name must be 1-48 characters: letters, numbers, spaces, - _ ' (and start with a letter or number)")

    size = path.stat().st_size
    if size == 0:
        fail(path, "file is empty")
        return
    if size > MAX_BYTES:
        fail(path, f"file is {size // 1024} KB, over the {MAX_BYTES // (1024 * 1024)} MB limit")
        return

    raw = path.read_bytes()
    if b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
        fail(path, "DOCTYPE/ENTITY declarations are not allowed")
        return

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        fail(path, f"not valid XML ({e}). Save the patch with KMISynth's Save... button")
        return

    if root.tag != "KMISynth":
        fail(path, f"root element is <{root.tag}>, expected <KMISynth>. Is this a KMISynth patch?")
        return

    tags = [t.strip() for t in root.get("tags", "").split(",") if t.strip()]
    if not tags:
        fail(path, "patch has no tags. In the preset browser, right-click the patch > Edit tags...")


def main() -> int:
    if not PATCHES.is_dir():
        print("::error::Patches/ folder not found")
        return 1

    seen: dict[tuple[str, str], Path] = {}
    count = 0

    for path in sorted(PATCHES.rglob("*")):
        if path.is_dir():
            continue
        parts = path.relative_to(PATCHES).parts

        if len(parts) != 2:
            fail(path, "patches go directly in a category folder: Patches/<Category>/<Name>.kmip")
            continue
        category, filename = parts
        if category not in CATEGORIES:
            fail(path, f"'{category}' is not a category. Use one of: {', '.join(sorted(CATEGORIES))}")
            continue
        if filename == ".gitkeep":
            continue
        if path.suffix.lower() != ".kmip":
            fail(path, "only .kmip patch files are allowed in Patches/")
            continue

        key = (category, path.stem.casefold())
        if key in seen:
            fail(path, f"name clashes with {seen[key].name} in the same folder")
        else:
            seen[key] = path

        check_patch(path)
        count += 1

    if errors:
        print(f"\n{len(errors)} problem(s) found in {count} patch file(s).")
        return 1
    print(f"All {count} patch file(s) OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
