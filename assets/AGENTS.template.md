# AGENTS.md

This file is the first thing an LLM session should read when working in this wiki, and it is the **canonical instructions for any AI agent** operating in this directory — regardless of which tool the agent is running under. Different LLM clients auto-load different filenames at session start: Anthropic's Claude Code reads `CLAUDE.md`, OpenAI's Codex / ChatGPT and many other tools read `AGENTS.md`, Cursor reads `.cursorrules`. This skill picks `AGENTS.md` as the single source of truth and routes Claude Code to it via a one-line `CLAUDE.md` stub at the wiki root.

Two kinds of content live here: **operational instructions** (how to use the wiki to answer questions, how to run maintenance scripts) and **wiki-specific conventions** (the project's domain, tag vocabulary, source-id rules, house rules). The operational sections are mostly the same across wikis built with this skill; the conventions vary per wiki and are what you customize after bootstrap. Keep each section short — if a section grows past a screen, the content probably wants to become a concept file or a meta note instead.

## Domain

<!--
One paragraph. What's this wiki about? The answer constrains what counts as
a source, what the tag vocabulary should look like, and how strict the
citation rules need to be.
-->

## Wiki retrieval protocol

When answering questions about topics in this wiki, follow this lookup order:

1. **Re-read this file (`AGENTS.md`)** for the domain, tag vocabulary, source-id conventions, and scope exclusions.
2. **Check `index.md`** at the wiki root for orientation — it is the portal page grouping all concepts and sources.
3. **Check `indices/aliases.json`** to resolve concept names — concepts often have multiple aliases.
4. **Use `indices/backlinks.json`** to find which concepts reference a given concept, and `indices/orphans.json` for red-link frontier concepts.
5. **Read the relevant `concepts/` and `sources/` files** — every non-trivial claim in a concept article has a footnote citation traceable to a specific anchor in a source file.
6. **Ground all answers in `sources/`** — do not answer from training data alone. If the wiki does not cover a topic, say so explicitly rather than generating an uncited answer.

## Boundary discipline

This wiki is the knowledge boundary for questions asked in this directory. If a topic is not covered by concept or source files in this wiki, respond with "this wiki does not cover that topic" rather than answering from general knowledge. The user can then decide whether to ingest new sources.

## Tag vocabulary

The controlled list of tags in use. Add to this deliberately — tag drift
(e.g. `ml` vs `machine-learning` vs `ML` all coexisting) is one of the main
ways wikis rot. Grep before adding a new tag.

- `example-tag` — when to use this tag

## Source id convention

Default: `lastname-year-shorttitle`, e.g. `vaswani-2017-attention`.

<!--
Override if your domain needs something different. Examples:
  - industry reports:     `org-year-title` (e.g. `oecd-2024-ai-outlook`)
  - blog posts:           `author-YYYYMMDD-title` (e.g. `karpathy-20230101-rnn`)
  - conversation logs:    `participant-YYYYMMDD-topic`
Whatever you pick, pick it once and stick to it.
-->

## Project-specific conventions

<!--
Anything else a future LLM session should know before editing this wiki.
Examples:
  - "never create a concept article from a single blog post — need a paper"
  - "math concepts cite the textbook by page number, not section"
  - "conversation transcripts go in sources/ with kind: conversation"
  - "status: stable requires at least two independent sources"
-->

## Wikilink policy

When writing or updating a concept article, if a related concept SHOULD exist in this wiki but does not yet have an article, link to it anyway using `[[concept-id]]`. Red links are a feature — they mark the wiki's growth frontier and feed the automated build queue.

A good concept article should produce 3–8 outbound wikilinks, of which at least 2–3 may be red links to concepts not yet written. If you finish writing a concept and it has zero red links, you are probably being too conservative — go back and add links to related concepts that a reader would reasonably want to look up.

Do NOT avoid red links to "keep things clean." A wiki with no red links is a wiki that has stopped growing.

## After any edit

Run in order:

```
python scripts/build_alias_index.py .
python scripts/build_backlinks.py .
python scripts/check_links.py .
python scripts/unused_claims.py .
```

A non-zero exit from `check_links.py` almost always means a hallucinated citation. Fix it before moving on. `unused_claims.py` surfaces source anchors not yet cited by any concept article — the supply-side growth queue.

## Status

- **Started**: <!-- YYYY-MM-DD -->
- **Last audit**: <!-- YYYY-MM-DD — last time you read a concept cold and checked citations -->
- **Size**: <!-- rough count of concepts / sources, updated occasionally -->
