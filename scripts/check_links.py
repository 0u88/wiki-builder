#!/usr/bin/env python3
"""Validate wikilinks and source citations.

Usage:
    python scripts/check_links.py <wiki-root>

For every .md file under concepts/, sources/, meta/, disambig/, every
[[wikilink]] is classified into one of two kinds, depending on its target:

  * SOURCE CITATION — the target's bare stem matches a file in sources/,
    OR the target uses Obsidian block-reference form `[[stem#^anchor]]`
    where the `#^` marker unambiguously indicates a citation. Source
    citations MUST resolve to a real sources/<stem>.md, and a `#^anchor`
    MUST match a block ID (a line ending in `^anchor`) inside that file.
    Either failure is a HARD ERROR (exit 1): a missing source means a
    hallucinated source, and a missing anchor means a hallucinated claim
    attributed to a real source, the more common failure.

  * CONCEPT LINK — anything else. Resolved through indices/aliases.json
    as a soft warning. Red concept links are a feature, not a bug: they
    show up in indices/orphans.json as the wiki's frontier markers.

Footnotes are checked too: every `[^N]` reference in a file must have a
matching `[^N]:` definition (HARD ERROR if not, because the claim is left
uncited), and a definition that nothing references is a warning.

Exits 0 if every source citation and footnote resolves, 1 otherwise. Designed to be
wired into a pre-commit hook. Run build_alias_index.py first.

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
# Obsidian block IDs: a line ending in ^anchor (same rule as unused_claims.py).
BLOCK_ID_RE = re.compile(r"\^([\w-]+)\s*$", re.MULTILINE)
FOOTNOTE_DEF_RE = re.compile(r"^\[\^([^\]\s]+)\]:", re.MULTILINE)
FOOTNOTE_REF_RE = re.compile(r"\[\^([^\]\s]+)\](?!:)")
NAMESPACES = ("concepts", "sources", "meta", "disambig")


def normalize(s: str) -> str:
    return s.strip().lower()


def split_target(target: str) -> tuple[str, str]:
    """Split a wikilink target into (stem, anchor_part).

    Examples:
        "foo"               -> ("foo", "")
        "foo#^bar"          -> ("foo", "#^bar")
        "foo#bar"           -> ("foo", "#bar")
        "foo|display text"  -> never reaches here; pipe is stripped by WIKILINK_RE
    """
    if "#" in target:
        stem, _, anchor = target.partition("#")
        return stem.strip(), "#" + anchor
    return target.strip(), ""


def strip_code(text: str) -> str:
    """Remove fenced code blocks and inline code spans before scanning.

    Wikilinks inside code are syntax examples, not real references.
    """
    text = FENCED_CODE_RE.sub("", text)
    text = INLINE_CODE_RE.sub("", text)
    return text


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_links.py <wiki-root>", file=sys.stderr)
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
    # source id -> block IDs declared in that source file
    anchors: dict[str, set[str]] = {}
    if sources_dir.is_dir():
        for p in sources_dir.glob("*.md"):
            anchors[p.stem] = set(BLOCK_ID_RE.findall(p.read_text(encoding="utf-8")))
    source_ids = set(anchors)

    bad_concept_links: list[tuple[str, str]] = []  # (file, target) — soft warnings
    bad_citations: list[tuple[str, str]] = []      # (file, source stem) — hard errors
    bad_anchors: list[tuple[str, str, str]] = []   # (file, stem, anchor) — hard errors
    undefined_notes: list[tuple[str, str]] = []    # (file, footnote label) — hard errors
    unused_notes: list[tuple[str, str]] = []       # (file, footnote label) — soft warnings
    n_files = 0

    for ns in NAMESPACES:
        d = root / ns
        if not d.is_dir():
            continue
        for path in sorted(d.glob("*.md")):
            n_files += 1
            text = path.read_text(encoding="utf-8")
            scannable = strip_code(text)
            rel = str(path.relative_to(root))
            defined = set(FOOTNOTE_DEF_RE.findall(scannable))
            referenced = set(FOOTNOTE_REF_RE.findall(scannable))
            undefined_notes += [(rel, n) for n in sorted(referenced - defined)]
            unused_notes += [(rel, n) for n in sorted(defined - referenced)]
            for raw_target in WIKILINK_RE.findall(scannable):
                # Inside markdown tables, the alias separator is escaped
                # as `\|`, which leaves a stray backslash on the captured
                # target. Strip it before resolving.
                raw_target = raw_target.rstrip("\\")
                stem, anchor = split_target(raw_target)
                # Block-reference style [[X#^Y]] is a source citation by
                # convention. The `^` marker is the tell — concept links
                # should never use it.
                if anchor.startswith("#^"):
                    if stem not in source_ids:
                        bad_citations.append((rel, stem))
                    elif anchor[2:].strip() not in anchors[stem]:
                        bad_anchors.append((rel, stem, anchor[2:].strip()))
                    continue
                # A bare [[X]] (or [[X#section]] heading link) where X
                # matches a source filename is also a source citation.
                if stem in source_ids:
                    continue  # exists, fine
                # Otherwise it's a concept link — resolve via aliases.
                if normalize(stem) not in aliases:
                    bad_concept_links.append((rel, raw_target.strip()))

    n_errors = len(bad_citations) + len(bad_anchors) + len(undefined_notes)
    print(
        f"checked {n_files} files: {len(bad_concept_links)} red concept links (warnings), "
        f"{len(unused_notes)} unused footnote definitions (warnings), "
        f"{n_errors} errors ({len(bad_citations)} unknown sources, "
        f"{len(bad_anchors)} unknown anchors, {len(undefined_notes)} undefined footnotes)"
    )

    if bad_concept_links:
        print("\nRED CONCEPT LINKS (informational — frontier of the wiki):", file=sys.stderr)
        for f, t in bad_concept_links:
            print(f"  {f}: [[{t}]]", file=sys.stderr)
    if unused_notes:
        print("\nUNUSED FOOTNOTE DEFINITIONS:", file=sys.stderr)
        for f, n in unused_notes:
            print(f"  {f}: [^{n}]", file=sys.stderr)
    if bad_citations:
        print("\nUNRESOLVED CITATIONS (likely hallucinated source):", file=sys.stderr)
        for f, k in bad_citations:
            print(f"  {f}: [[{k}#^...]]", file=sys.stderr)
    if bad_anchors:
        print("\nUNKNOWN ANCHORS (likely hallucinated claim in a real source):", file=sys.stderr)
        for f, k, a in bad_anchors:
            print(f"  {f}: [[{k}#^{a}]] — no ^{a} in sources/{k}.md", file=sys.stderr)
    if undefined_notes:
        print("\nUNDEFINED FOOTNOTES (claim left uncited):", file=sys.stderr)
        for f, n in undefined_notes:
            print(f"  {f}: [^{n}] has no [^{n}]: definition", file=sys.stderr)

    # Red concept links are a feature, not an error — they show up in
    # indices/orphans.json as frontier hints. Only citation problems block,
    # because they almost always indicate hallucinated sources or claims.
    return 1 if n_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
