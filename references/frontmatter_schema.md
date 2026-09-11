# Frontmatter schema reference

This file is loaded on demand when the LLM needs the precise field-by-field
schema for any of the four file kinds (`concepts`, `sources`, `meta`,
`disambig`). The short version lives in `SKILL.md`; this file is the
authoritative spec.

The helper scripts use a deliberately minimal YAML parser that supports only
two value types: scalars (optionally quoted) and inline lists `[a, b, c]`.
Don't introduce nested mappings, multi-line strings, or block lists — they
won't parse.

## concepts/*.md

| Field      | Required | Type        | Notes                                                                          |
| ---------- | -------- | ----------- | ------------------------------------------------------------------------------ |
| `id`       | yes      | string      | Must equal filename stem. Lowercase slug, hyphen-separated.                    |
| `title`    | yes      | string      | Display title. Use proper capitalization and full words.                       |
| `aliases`  | no       | list[str]   | Other names that should resolve to this concept. Case-insensitive at lookup.   |
| `tags`     | no       | list[str]   | Topical tags from the controlled vocabulary in `AGENTS.md`.                    |
| `status`   | yes      | enum        | One of `stub`, `draft`, `stable`. Be honest — don't mark stubs as stable.      |
| `created`  | yes      | date        | ISO date `YYYY-MM-DD`.                                                         |
| `updated`  | yes      | date        | ISO date. Bump on every non-trivial edit.                                      |
| `sources`  | no       | list[str]   | Source ids cited in this article. Should match the source-id stems used in `[[stem#^anchor]]` block-reference citations in the body. |

## sources/*.md

| Field       | Required | Type      | Notes                                                                                     |
| ----------- | -------- | --------- | ----------------------------------------------------------------------------------------- |
| `id`        | yes      | string    | Must equal filename stem. Convention: `lastname-year-shorttitle`, e.g. `vaswani-2017-attention`. |
| `title`     | yes      | string    | Quote it if it contains a colon.                                                          |
| `authors`   | no       | list[str] | Surnames are fine; full names if you want.                                                |
| `year`      | no       | int       | Publication year.                                                                         |
| `kind`      | yes      | enum      | One of `paper`, `article`, `repo`, `dataset`, `video`, `conversation`, `other`.           |
| `url`       | no       | string    | Canonical URL of the source.                                                              |
| `raw`       | no       | string    | Path (relative to wiki root) to a local copy in `raw/`. Strongly recommended.             |
| `ingested`  | yes      | date      | ISO date when this source was added to the wiki.                                          |

## meta/*.md

No required frontmatter. These are free-form editorial notes that mirror a
concept file by name (e.g. `meta/transformer-ml.md` mirrors
`concepts/transformer-ml.md`). Use them for: open questions, things you
weren't sure how to classify, disagreements between sources, things to revisit.

## disambig/*.md

| Field  | Required | Type   | Notes                                |
| ------ | -------- | ------ | ------------------------------------ |
| `id`   | yes      | string | Must equal filename stem.            |
| `kind` | yes      | const  | Must be the literal string `disambiguation`. |

The body must list all candidate meanings as wikilinks.

## Inline syntax (in article body)

| Construct               | Syntax                                          | Resolves to                                                                  |
| ----------------------- | ----------------------------------------------- | ---------------------------------------------------------------------------- |
| Concept link            | `[[concept-id]]`                                | `concepts/<concept-id>.md` (via alias index)                                 |
| Concept link with alias | `[[concept-id\|display text]]`                  | Same target, custom display text                                             |
| Source citation (body)  | `claim text[^N].`                               | A markdown footnote reference, flush against the cited text, no leading space |
| Notes section heading   | `## Notes`                                      | Always the last section of a concept file when any source citations are used |
| Notes entry             | `[^N]: [[source-id#^anchor\|Author Year, §anchor]]` | The actual source link — Obsidian block reference to a `^anchor` in the source file |

**Source citations follow the Wikipedia/academic-paper convention.** In the body of a concept article each cited claim ends with a numbered footnote reference `[^N]`; the actual source wikilink lives in a `## Notes` section at the bottom of the same file. Per-file numbering — each concept article restarts at `[^1]`. Same target → same number; different anchor of the same source → different number.

The display text in each Notes entry is derived mechanically from the source-id `<lastname>-<year>-<slug>` → `Lastname Year, §anchor`, with `a`/`b`/`c` suffixes when two sources share the same author and year. Keeping this mechanical means future LLM sessions don't have to invent display text by hand.

Footnote references inside markdown table cells need no escaping: `| burial | unknown[^1] |` is unambiguous, unlike a raw wikilink which would need `\|` inside the cell.

**Citations vs concept links.** Both kinds use `[[…]]` syntax, distinguished by what the target resolves to:

- The `#^` marker (Obsidian block reference) unambiguously identifies a source citation. Concept links should never use `#^`.
- Bare `[[X]]` is interpreted as a source citation if `X` matches a filename in `sources/`, otherwise as a concept link.
- The bare-stem ambiguity is harmless in practice because a wiki shouldn't have both a concept and a source with the same id (it would clash).

The concept-link lookup is case-insensitive (the alias index normalizes everything to lowercase). Source-id stems are case-sensitive — they must match the filename stem exactly.

**Source files must place block IDs at the end of each "Key claims" bullet** so that block-reference citations resolve. The convention is:

```markdown
- **thm-1**: The PPI confidence interval has valid coverage… ^thm-1
- **sec-3.2**: Width of the interval scales with the rectifier variance… ^sec-3.2
```

The bold prefix is for visual scanning when reading the source file directly; the trailing `^anchor` is the actual Obsidian block ID. Keep them identical so the link target is unambiguous.

## What `check_links.py` validates

Each `[[wikilink]]` in the file (whether in the body or the `## Notes` section) is classified into one of two kinds and validated accordingly:

1. **Source citation** — block-reference form `[[X#^Y]]`, or bare `[[X]]` where X matches a file in `sources/`. The `X` stem must resolve to a real `sources/<X>.md` file. **Hard error** — an unresolved citation exits non-zero, because it almost always indicates a hallucinated source. Most source-citation wikilinks live inside `## Notes` entries (`[^N]: [[X#^Y|Author Year, §Y]]`), but the validation does not depend on position — any source wikilink anywhere in a file is checked.
2. **Concept link** — everything else. The bare stem (without any `#anchor` part) is resolved through the alias index. **Warning only** — red concept links are listed but do not cause a non-zero exit, because they're treated as a feature (frontier markers in `orphans.json`).

It does **not** validate:

- That every `[^N]` footnote reference in the body has a matching `[^N]:` definition in the Notes section, or vice versa. (Markdown renderers like Obsidian will surface broken footnotes visually. The conversion script that introduces footnotes generates both reference and definition together, so manual edits are the only way they can drift apart.)
- That the block-ID anchor `#^xxx` actually exists inside the source file.
  (Anchors are free-form strings; validating them would require a separate
  inventory in each source file. Obsidian itself will flag a click-through
  to a missing block ID.)
- That a `[[concept-id#section]]` heading anchor exists in the target concept
  file. The script resolves the bare stem and ignores the heading part.
- That tags come from a controlled vocabulary. (Use `grep` and `AGENTS.md`
  for that.)
- That `sources` listed in concept frontmatter match the citations actually
  used in the body. (Could be added; currently not.)
