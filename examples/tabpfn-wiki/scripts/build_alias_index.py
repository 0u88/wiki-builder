#!/usr/bin/env python3
"""Build indices/aliases.json from concept frontmatter.

Usage:
    python scripts/build_alias_index.py <wiki-root>

Reads every concepts/*.md file, extracts the `id` and `aliases` fields
from frontmatter, and writes a flat mapping from each normalized alias
(and the canonical id itself) to the canonical id.

Errors out non-zero on conflicts: two concepts claiming the same alias,
or an alias whose normalized form collides with another concept's id.

Stdlib only. Designed to be copied verbatim into a wiki's own scripts/.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def strip_inline_comment(val: str) -> str:
    """Strip a trailing ``# comment`` unless the ``#`` is inside quotes.

    Follows the YAML convention that an inline comment must be preceded by
    whitespace (so ``url: https://x/#frag`` is not mangled, but
    ``status: stub   # pick one of stub|draft|stable`` is).
    """
    in_single = False
    in_double = False
    for i, ch in enumerate(val):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            if i == 0 or val[i - 1].isspace():
                return val[:i].rstrip()
    return val


def parse_frontmatter(text: str) -> dict:
    """Minimal YAML frontmatter parser. Handles scalars and inline lists."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    body = text[3:end].strip()
    out: dict = {}
    for line in body.splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = strip_inline_comment(val.strip()).strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            out[key] = (
                [i.strip().strip('"').strip("'") for i in inner.split(",") if i.strip()]
                if inner
                else []
            )
        else:
            out[key] = val.strip('"').strip("'")
    return out


def normalize(s: str) -> str:
    return s.strip().lower()


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: build_alias_index.py <wiki-root>", file=sys.stderr)
        return 2
    root = Path(argv[1]).resolve()
    concepts = root / "concepts"
    if not concepts.is_dir():
        print(f"no concepts/ directory at {root}", file=sys.stderr)
        return 2

    index: dict[str, str] = {}
    conflicts: list[str] = []
    n = 0

    for path in sorted(concepts.glob("*.md")):
        n += 1
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        cid = fm.get("id") or path.stem
        if cid != path.stem:
            print(
                f"warning: {path.name} declares id={cid!r} but stem is {path.stem!r}",
                file=sys.stderr,
            )

        keys = [cid]
        aliases = fm.get("aliases") or []
        if isinstance(aliases, list):
            keys.extend(aliases)

        for k in keys:
            if not k:
                continue
            nk = normalize(k)
            if not nk:
                continue
            if nk in index and index[nk] != cid:
                conflicts.append(f"{k!r} -> both {index[nk]!r} and {cid!r}")
            else:
                index[nk] = cid

    out_dir = root / "indices"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "aliases.json"
    out_path.write_text(
        json.dumps(index, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"wrote {out_path.relative_to(root)} ({len(index)} entries from {n} concepts)")
    if conflicts:
        print(f"\n{len(conflicts)} alias conflict(s):", file=sys.stderr)
        for c in conflicts:
            print(f"  {c}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
