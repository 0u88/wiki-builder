#!/usr/bin/env python3
"""Build indices/backlinks.json and indices/orphans.json.

Usage:
    python scripts/build_backlinks.py <wiki-root>

Scans every .md file under concepts/, sources/, meta/, disambig/ for
[[wikilinks]], resolves each through indices/aliases.json, and writes:

    indices/backlinks.json   concept_id -> sorted list of files linking to it
    indices/orphans.json     unresolved concept links: target -> sorted list of files

Source citations (block-reference form [[X#^Y]] or bare [[X]] where X is
a source filename) are deliberately **excluded** from both indices —
they are validated separately by check_links.py and would otherwise
create noise in the concept backlink/orphan view.

Run build_alias_index.py FIRST — this script depends on indices/aliases.json.
Stdlib only. Designed to be copied verbatim into a wiki's own scripts/.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

WIKILINK_RE = re.compile(r"\[\[([^\]\|]+)(?:\|[^\]]*)?\]\]")
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
NAMESPACES = ("concepts", "sources", "meta", "disambig")


def normalize(s: str) -> str:
    return s.strip().lower()


def split_target(target: str) -> tuple[str, str]:
    """Split a wikilink target into (stem, anchor_part).

    Examples:
        "foo"          -> ("foo", "")
        "foo#^bar"     -> ("foo", "#^bar")  # block reference (source citation)
        "foo#bar"      -> ("foo", "#bar")   # heading link (concept section)
    """
    if "#" in target:
        stem, _, anchor = target.partition("#")
        return stem.strip(), "#" + anchor
    return target.strip(), ""


def strip_code(text: str) -> str:
    """Remove fenced code blocks and inline code spans before scanning.

    Wikilinks and citations inside code are syntax examples, not real
    references — we don't want them counted as backlinks or red links.
    """
    text = FENCED_CODE_RE.sub("", text)
    text = INLINE_CODE_RE.sub("", text)
    return text


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: build_backlinks.py <wiki-root>", file=sys.stderr)
        return 2
    root = Path(argv[1]).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    aliases_path = root / "indices" / "aliases.json"
    if not aliases_path.exists():
        print(
            f"missing {aliases_path.relative_to(root)} — run build_alias_index.py first",
            file=sys.stderr,
        )
        return 2
    aliases: dict[str, str] = json.loads(aliases_path.read_text(encoding="utf-8"))

    sources_dir = root / "sources"
    source_ids: set[str] = set()
    if sources_dir.is_dir():
        source_ids = {p.stem for p in sources_dir.glob("*.md")}

    backlinks: dict[str, set[str]] = {}
    orphans: dict[str, set[str]] = {}
    n_files = 0
    n_links = 0
    n_citations_skipped = 0

    for ns in NAMESPACES:
        d = root / ns
        if not d.is_dir():
            continue
        for path in sorted(d.glob("*.md")):
            n_files += 1
            text = path.read_text(encoding="utf-8")
            scannable = strip_code(text)
            rel = str(path.relative_to(root))
            for raw_target in WIKILINK_RE.findall(scannable):
                n_links += 1
                # Inside markdown tables, the alias separator is escaped
                # as `\|`, which leaves a stray backslash on the captured
                # target. Strip it before resolving.
                raw_target = raw_target.rstrip("\\")
                stem, anchor = split_target(raw_target)
                # Source citations are tracked by check_links.py, not here.
                # The two recognized forms are [[X#^Y]] (block reference) or
                # bare [[X]] where X happens to be a source filename.
                if stem in source_ids or anchor.startswith("#^"):
                    n_citations_skipped += 1
                    continue
                # Concept link — resolve the bare stem (heading anchors are
                # ignored at this stage; the file as a whole is the target).
                resolved = aliases.get(normalize(stem))
                if resolved:
                    # Don't list a file as backlinking to itself.
                    if not (ns == "concepts" and path.stem == resolved):
                        backlinks.setdefault(resolved, set()).add(rel)
                else:
                    orphans.setdefault(raw_target.strip(), set()).add(rel)

    indices_dir = root / "indices"
    indices_dir.mkdir(exist_ok=True)

    backlinks_out = {k: sorted(v) for k, v in sorted(backlinks.items())}
    orphans_out = {k: sorted(v) for k, v in sorted(orphans.items())}

    (indices_dir / "backlinks.json").write_text(
        json.dumps(backlinks_out, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (indices_dir / "orphans.json").write_text(
        json.dumps(orphans_out, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(
        f"scanned {n_files} files, {n_links} wikilinks "
        f"({n_citations_skipped} source citations excluded); "
        f"{len(backlinks_out)} concepts have inbound links, "
        f"{len(orphans_out)} red concept links"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
