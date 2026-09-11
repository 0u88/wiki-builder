#!/usr/bin/env python3
"""Bootstrap a new wiki directory with the standard wiki-builder layout.

Usage:
    python scripts/bootstrap_wiki.py <wiki-root>

Creates the directory tree, copies the three helper scripts into the new
wiki's own ``scripts/`` directory so the wiki is self-contained, scaffolds
an ``AGENTS.md`` (canonical agent-instructions file: retrieval protocol
plus wiki-specific conventions), a one-line ``CLAUDE.md`` stub routing
Claude Code to ``AGENTS.md``, and an ``index.md`` portal page from the
bundled templates, and seeds empty indices by running the alias and
backlink builders once.

The bootstrap script itself is NOT copied into the new wiki — it's a
one-shot setup tool, not part of the ongoing maintenance loop.

Refuses to run against a non-empty directory to avoid clobbering work.

Stdlib only.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

# Directories that make up a wiki. Order doesn't matter; they're all created.
NAMESPACES = ("concepts", "sources", "meta", "disambig", "raw", "scripts", "indices")

# Helper scripts that get copied into the new wiki's scripts/ directory.
# bootstrap_wiki.py is deliberately NOT in this list.
HELPERS = ("build_alias_index.py", "build_backlinks.py", "check_links.py")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: bootstrap_wiki.py <wiki-root>", file=sys.stderr)
        return 2

    root = Path(argv[1]).resolve()
    skill_scripts = Path(__file__).resolve().parent
    skill_root = skill_scripts.parent
    agents_template_path = skill_root / "assets" / "AGENTS.template.md"
    claude_template_path = skill_root / "assets" / "CLAUDE.template.md"
    index_template_path = skill_root / "assets" / "index.template.md"

    if root.exists() and any(root.iterdir()):
        print(
            f"refusing to bootstrap into non-empty directory: {root}\n"
            f"(move or delete its contents first, or pick a new path)",
            file=sys.stderr,
        )
        return 2

    root.mkdir(parents=True, exist_ok=True)
    for ns in NAMESPACES:
        (root / ns).mkdir(exist_ok=True)

    # Copy helper scripts into the wiki's own scripts/ so the wiki is
    # self-contained and can be version-controlled independently of the skill.
    copied = []
    for name in HELPERS:
        src = skill_scripts / name
        if not src.exists():
            print(f"warning: helper {name} not found at {src}", file=sys.stderr)
            continue
        shutil.copy2(src, root / "scripts" / name)
        copied.append(name)

    # Scaffold AGENTS.md from the bundled template. If the template is
    # missing (someone pruned assets/), fall back to a minimal stub so the
    # bootstrap still produces a working wiki.
    agents_path = root / "AGENTS.md"
    if agents_template_path.exists():
        shutil.copy2(agents_template_path, agents_path)
    else:
        agents_path.write_text(
            "# AGENTS.md\n\n"
            "(fill in: domain, controlled tag vocabulary, source id convention, "
            "project-specific conventions)\n",
            encoding="utf-8",
        )

    # Scaffold CLAUDE.md as a one-line stub routing Claude Code to AGENTS.md.
    # AGENTS.md is the canonical cross-tool agent-instructions file; CLAUDE.md
    # exists only because Claude Code auto-loads that filename at session start.
    # Keeping CLAUDE.md as a stub (rather than duplicating AGENTS.md content)
    # avoids drift between the two files. Same fallback pattern as AGENTS.md.
    claude_path = root / "CLAUDE.md"
    if claude_template_path.exists():
        shutil.copy2(claude_template_path, claude_path)
    else:
        claude_path.write_text(
            "# Claude Instructions\n\n"
            "All instructions for AI sessions in this wiki are in `AGENTS.md` "
            "— that is the canonical, cross-tool agent-instructions file. "
            "Read it first.\n",
            encoding="utf-8",
        )

    # Scaffold index.md from the bundled template. This is the wiki's
    # portal page — the only file that lives at the wiki root rather than
    # under a namespace, because it is a navigation aid maintained by hand
    # rather than content. The maintenance scripts deliberately ignore it.
    # Same fallback pattern as AGENTS.md.
    index_path = root / "index.md"
    if index_template_path.exists():
        shutil.copy2(index_template_path, index_path)
    else:
        index_path.write_text(
            "# [Wiki title]\n\n"
            "Portal page. Edit by hand to group concepts the way a reader "
            "would actually look for them. Use [[wikilink]] syntax.\n",
            encoding="utf-8",
        )

    # Seed empty indices by running the alias + backlink builders once.
    # We ignore their exit codes here — the wiki is empty, there's nothing
    # meaningful to fail on, and any real issues will surface on the first
    # real edit when the user runs check_links.py.
    python = sys.executable
    for script in ("build_alias_index.py", "build_backlinks.py"):
        script_path = root / "scripts" / script
        if script_path.exists():
            subprocess.run([python, str(script_path), str(root)], check=False)

    print(f"\nbootstrapped wiki at {root}")
    print(f"  copied {len(copied)} helper scripts into scripts/")
    print(f"  scaffolded AGENTS.md (canonical agent instructions)")
    print(f"  scaffolded CLAUDE.md (stub routing to AGENTS.md)")
    print(f"  scaffolded index.md (portal page)")
    print(f"  seeded empty indices in indices/")
    print()
    print("next steps:")
    print("  1. edit AGENTS.md — record your domain, tag vocabulary, id convention")
    print("  2. drop raw sources into raw/")
    print("  3. ask Claude (with the wiki-builder skill) to ingest them")
    print("  4. update index.md as concepts are added — it is your portal page")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
