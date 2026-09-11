# LLM retrieval setup (post-bootstrap and retrofit)

This file covers three pieces of LLM-retrieval setup for a wiki: (1) the `CLAUDE.md` stub that routes Claude Code to the canonical `AGENTS.md`, (2) an optional `/wiki` slash command for explicit wiki-grounded Q&A, and (3) wiring `check_links.py` into a git pre-commit hook so hallucinated citations are blocked before they enter the history.

For **new wikis**: `bootstrap_wiki.py` auto-creates the `CLAUDE.md` stub from `assets/CLAUDE.template.md`, so item (1) is already done at bootstrap time. The manual post-bootstrap steps are just (3) the pre-commit hook, and optionally (2) the `/wiki` command.

For **retrofitting an existing wiki** that predates the canonical-`AGENTS.md` pattern: its `CLAUDE.md` is likely a full retrieval-protocol copy, and its `AGENTS.md` is conventions-only. Replace `CLAUDE.md` with the stub below, and add the missing operational sections (`Wiki retrieval protocol`, `Boundary discipline`, `After any edit`) into `AGENTS.md` — see `assets/AGENTS.template.md` for the canonical structure.

## Why CLAUDE.md is a stub, not a copy

`AGENTS.md` is the canonical instructions file for AI sessions working in the wiki. It contains both the **operational retrieval protocol** (lookup order, boundary discipline, post-edit script sequence) AND the wiki's **domain-specific conventions** (tag vocabulary, source-id format, project house rules). The bootstrap script scaffolds it from `assets/AGENTS.template.md`, and the user customizes the convention sections immediately after bootstrap.

Different LLM clients have their own conventions for which file they auto-read at session start: Anthropic's Claude Code reads `CLAUDE.md`, OpenAI's Codex / ChatGPT and many other tools read `AGENTS.md`, Cursor reads `.cursorrules`. This skill picks `AGENTS.md` as the single source of truth (it is the cross-tool standard) and routes Claude Code to it via a one-line stub, rather than maintaining two near-identical files that will drift over time.

A stub file rather than a symlink because Windows symlinks need admin / developer mode and aren't reliable across platforms; a stub works everywhere.

## CLAUDE.md stub

Drop this into the wiki root as `CLAUDE.md`:

```markdown
# Claude Instructions

All instructions for AI sessions in this wiki are in `AGENTS.md` — that is the canonical, cross-tool agent-instructions file. Read it first.
```

That is the entire file. No customization needed; the same stub works for every wiki.

## Optional: `/wiki` slash command for explicit wiki-only Q&A

Once `CLAUDE.md` routes any session to `AGENTS.md`, Claude Code automatically follows the retrieval protocol. The `/wiki` slash command is therefore mostly redundant — but still useful in two cases: (1) when the user wants to force wiki-only mode in a session that has already drifted into general-knowledge answering, or (2) for users who prefer an explicit command over relying on auto-loaded instructions.

Drop this into `<wiki-root>/.claude/commands/wiki.md`:

```markdown
# /wiki

Ask a question grounded in this wiki's source material.

## Instructions

Follow the **Wiki retrieval protocol** in `AGENTS.md`. Treat this wiki as your sole knowledge source — do not supplement with training data. If the wiki does not contain enough information to answer, say so and identify which sources or concepts would need to be added.

Report which files you consulted at the end of your answer, with source-id and anchor (e.g. "Author Year, §sec-3") so the user can verify.

## Question

$ARGUMENTS
```

Skip this step if the wiki is small or the user is the only consumer — the auto-loaded `AGENTS.md` already enforces wiki-grounded answers.

## Wiring check_links.py into a pre-commit hook

Hallucinated citations are the main failure mode this skill guards against, and `check_links.py` is the line of defence — but only if it actually runs. The simplest way to guarantee that is a git pre-commit hook. Drop this into `<wiki-root>/.git/hooks/pre-commit` and make it executable:

```bash
#!/usr/bin/env bash
set -e
python scripts/build_alias_index.py . >/dev/null
python scripts/check_links.py .
```

The alias index needs to be rebuilt first because `check_links.py` resolves wikilinks through it. If `check_links.py` exits non-zero (an unresolved source-citation wikilink anywhere in the file — typically in a `## Notes` section entry), the commit is blocked — catching the hallucination before it enters the history. Red concept links are only warnings and won't block, because they're intentional frontier markers.

For users who prefer the [pre-commit.com](https://pre-commit.com) framework, the equivalent `.pre-commit-config.yaml` hook is a `local` repo entry running the same two commands.
