#!/usr/bin/env python3
"""Validate every relative link, its shape, and the line-count table in this skill.

Usage:
    python scripts/check-links.py [ROOT]

ROOT defaults to the parent directory of this script. Exits 0 only when:

1. every relative link resolves to an existing file and every `#anchor`
   matches a heading in the target file;
2. no link target is followed by a stray `)` and no `#anchor` is written
   outside the parentheses — malformed shapes that plain target resolution
   cannot see;
3. every line count listed in `references/index.md` matches the real file.

External http(s) links are not fetched, and this is not a markdown linter.
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*([^)\s]+?)(?:\s+\"[^\"]*\")?\s*\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")

# `[x](a.md))` — target closed, then one more `)`. The link still resolves,
# so only a shape check can catch it.
STRAY_PAREN_RE = re.compile(r"\]\(\s*([^()\s]+?\.md)\s*\)\)")
# `[x](a.md)#anchor` — the anchor fell outside the parentheses.
ANCHOR_OUTSIDE_RE = re.compile(r"\]\(\s*([^()\s]+?\.md)\s*\)#")
# `| 3 | [stage/02](stage/02.md) | 执行 | 74 |`
COUNT_ROW_RE = re.compile(
    r"^\|\s*\d+\s*\|\s*\[[^\]]*\]\(([^)]+)\)\s*\|[^|]*\|\s*(\d+)\s*\|\s*$"
)


def slug(text: str) -> str:
    """GitHub-style heading anchor for CJK and latin headings."""
    text = INLINE_CODE_RE.sub(lambda m: m.group(0).strip("`"), text)
    text = text.strip().lower()
    out = []
    for ch in text:
        if ch in " -\t":
            out.append("-" if ch in " \t" else "-")
            continue
        cat = unicodedata.category(ch)
        if cat[0] in ("L", "N") or cat in ("Mn", "Mc") or ch == "_":
            out.append(ch)
    return "".join(out)


def headings(path: Path) -> set[str]:
    seen: dict[str, int] = {}
    anchors: set[str] = set()
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if not m:
            continue
        base = slug(m.group(2))
        count = seen.get(base, 0)
        seen[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def iter_md(root: Path):
    for p in sorted(root.rglob("*.md")):
        if any(part in {".git", "node_modules", ".trash"} for part in p.parts):
            continue
        yield p


def line_total(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def check_counts(root: Path, bad: list[str]) -> int:
    """Compare references/index.md's line-count table with the real files."""
    index = root / "references" / "index.md"
    if not index.is_file():
        return 0
    rows = 0
    for lineno, line in enumerate(index.read_text(encoding="utf-8").splitlines(), 1):
        m = COUNT_ROW_RE.match(line.strip())
        if not m:
            continue
        rel_path, claimed = m.group(1), int(m.group(2))
        rows += 1
        dest = (index.parent / rel_path).resolve()
        if not dest.is_file():
            bad.append(f"references/index.md:{lineno}  count table lists a missing file -> {rel_path}")
            continue
        actual = line_total(dest)
        if actual != claimed:
            bad.append(
                f"references/index.md:{lineno}  line count {claimed} != {actual} -> {rel_path}"
            )
    return rows


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else __file__).resolve()
    if root.is_file():
        root = root.parent
        if root.name == "scripts":
            root = root.parent
    root = root.resolve()

    cache: dict[Path, set[str]] = {}
    bad: list[str] = []
    checked = 0
    malformed = 0
    md_files = list(iter_md(root))

    for md in md_files:
        rel_src = md.relative_to(root).as_posix()
        in_fence = False
        for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            if FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue

            for m in STRAY_PAREN_RE.finditer(line):
                malformed += 1
                bad.append(
                    f"{rel_src}:{lineno}  extra ')' after target -> {m.group(1)}"
                )
            for m in ANCHOR_OUTSIDE_RE.finditer(line):
                malformed += 1
                bad.append(
                    f"{rel_src}:{lineno}  anchor outside parentheses -> {m.group(1)}#…"
                )

            for m in LINK_RE.finditer(line):
                target = m.group(1)
                if target.startswith(("http://", "https://", "mailto:", "tel:")):
                    continue
                checked += 1
                path_part, _, anchor = target.partition("#")
                if path_part:
                    dest = (md.parent / path_part).resolve()
                    if not dest.exists():
                        bad.append(f"{rel_src}:{lineno}  missing file   -> {target}")
                        continue
                else:
                    dest = md
                if anchor:
                    anchors = cache.get(dest)
                    if anchors is None:
                        anchors = headings(dest)
                        cache[dest] = anchors
                    if anchor not in anchors:
                        bad.append(f"{rel_src}:{lineno}  missing anchor -> {target}  (in {dest.name})")
                        continue
                if not str(dest).startswith(str(root)) and path_part:
                    bad.append(f"{rel_src}:{lineno}  escapes root   -> {target}")

    count_rows = check_counts(root, bad)

    print(f"root      : {root}")
    print(f"md files  : {len(md_files)}")
    print(f"links     : {checked} relative links checked")
    print(f"shape     : {malformed} malformed link shapes (extra ')', anchor outside parens)")
    print(f"counts    : {count_rows} rows of references/index.md line-count table checked")
    if bad:
        print(f"BAD       : {len(bad)}")
        for line in bad:
            print("  " + line)
        return 1
    print("BAD       : 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
