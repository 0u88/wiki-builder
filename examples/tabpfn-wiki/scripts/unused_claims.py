#!/usr/bin/env python3
"""Find source key claims that are not cited by any concept article.

Usage:
    python scripts/unused_claims.py <wiki-root>

Scans every sources/*.md file for Obsidian block-id anchors (lines
ending with ^anchor-name), then checks whether each anchor is cited
anywhere in concepts/*.md or meta/*.md via [[source-id#^anchor]] style
wikilinks. Claims that exist in source files but are never cited are
"orphan claims" — material that has been ingested but not yet
synthesized into concept articles.

Output: a priority-sorted list of unused claims, grouped by source,
along with a JSON file at indices/unused_claims.json for programmatic
consumption.

Stdlib only. Designed to be copied into a wiki's own scripts/.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Matches Obsidian block-id anchors: lines ending with ^anchor-name
BLOCK_ID_RE = re.compile(r"\^([\w-]+)\s*$", re.MULTILINE)

# Matches wikilinks that reference a block anchor: [[stem#^anchor...]]
BLOCK_REF_RE = re.compile(r"\[\[([^\]\|#]+)#\^([\w-]+)(?:\|[^\]]*)?\]\]")

# Also check footnote-style references that point to block anchors
# e.g. [^1]: [[source-id#^anchor|display text]]
FOOTNOTE_BLOCK_REF_RE = re.compile(r"\[\^[^\]]+\]:\s*\[\[([^\]\|#]+)#\^([\w-]+)(?:\|[^\]]*)?\]\]")

FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")

SCAN_NAMESPACES = ("concepts", "meta", "disambig")


def strip_code(text: str) -> str:
    text = FENCED_CODE_RE.sub("", text)
    text = INLINE_CODE_RE.sub("", text)
    return text


def find_declared_claims(root: Path) -> dict[str, list[str]]:
    """Return {source_id: [anchor1, anchor2, ...]} for all source files."""
    sources_dir = root / "sources"
    if not sources_dir.is_dir():
        return {}
    result: dict[str, list[str]] = {}
    for path in sorted(sources_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        anchors = BLOCK_ID_RE.findall(text)
        if anchors:
            result[path.stem] = sorted(anchors)
    return result


def find_cited_claims(root: Path) -> set[tuple[str, str]]:
    """Return {(source_id, anchor)} for all block-ref citations found."""
    cited: set[tuple[str, str]] = set()
    for ns in SCAN_NAMESPACES:
        d = root / ns
        if not d.is_dir():
            continue
        for path in sorted(d.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            scannable = strip_code(text)
            for stem, anchor in BLOCK_REF_RE.findall(scannable):
                cited.add((stem.strip(), anchor.strip()))
            for stem, anchor in FOOTNOTE_BLOCK_REF_RE.findall(scannable):
                cited.add((stem.strip(), anchor.strip()))
    # Also scan source files themselves — one source may cite another
    sources_dir = root / "sources"
    if sources_dir.is_dir():
        for path in sorted(sources_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            scannable = strip_code(text)
            for stem, anchor in BLOCK_REF_RE.findall(scannable):
                cited.add((stem.strip(), anchor.strip()))
            for stem, anchor in FOOTNOTE_BLOCK_REF_RE.findall(scannable):
                cited.add((stem.strip(), anchor.strip()))
    return cited


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: unused_claims.py <wiki-root>", file=sys.stderr)
        return 2
    root = Path(argv[1]).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    declared = find_declared_claims(root)
    cited = find_cited_claims(root)

    # Find unused claims
    unused: dict[str, list[str]] = {}
    total_declared = 0
    total_cited = 0
    total_unused = 0

    for source_id, anchors in sorted(declared.items()):
        source_unused = []
        for anchor in anchors:
            total_declared += 1
            if (source_id, anchor) in cited:
                total_cited += 1
            else:
                source_unused.append(anchor)
                total_unused += 1
        if source_unused:
            unused[source_id] = source_unused

    # Print human-readable summary
    print(f"claims: {total_declared} declared, {total_cited} cited, {total_unused} unused")
    print()

    sorted_sources = sorted(unused.items(), key=lambda x: -len(x[1]))

    if unused:
        print(f"unused claims by source ({len(sorted_sources)} sources with gaps):\n")
        for source_id, anchors in sorted_sources:
            total_in_source = len(declared[source_id])
            n_unused = len(anchors)
            pct = int(100 * n_unused / total_in_source) if total_in_source else 0
            print(f"  {source_id} ({n_unused}/{total_in_source} unused, {pct}%):")
            for anchor in anchors:
                print(f"    ^{anchor}")
            print()
    else:
        print("all claims are cited — no orphan claims found")

    # Write JSON for programmatic consumption (always, so consumers can
    # distinguish "no unused claims" from "script never ran"). When every
    # claim is cited the file is an empty object {}.
    indices_dir = root / "indices"
    indices_dir.mkdir(exist_ok=True)
    out_path = indices_dir / "unused_claims.json"

    json_data: dict[str, dict] = {}
    for source_id, anchors in sorted_sources:
        json_data[source_id] = {
            "total_claims": len(declared[source_id]),
            "unused_claims": anchors,
            "unused_count": len(anchors),
            "utilization_pct": round(
                100 * (1 - len(anchors) / len(declared[source_id])), 1
            )
            if declared[source_id]
            else 100.0,
        }

    out_path.write_text(
        json.dumps(json_data, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {out_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
