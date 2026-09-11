# [Wiki title — replace this]

<!--
This is the wiki's portal page — the file a human reader (or future you)
opens first to find their way around. It is the only file in the wiki that
lives at the root rather than under a namespace, because it is a navigation
aid, not a content page. Keep it that way:

- Edit it by hand. The maintenance scripts deliberately do NOT scan it,
  so wikilinks here will not pollute backlinks.json.
- Group concepts the way a reader would actually look for them — by topic,
  by chronology, by importance — not the way the filesystem stores them.
- Use [[wikilink]] syntax. In Obsidian (and most wiki-aware viewers) the
  links will be clickable.
- Update it whenever you add a major concept or finish a thematic cluster.
  A stale portal is worse than no portal.

Replace every section below as the wiki grows. Sections marked "(remove if
empty)" should be deleted entirely until they have content — empty sections
make the portal feel hollow.
-->

One- or two-sentence introduction to what this wiki is about and what its scope is. State explicitly what is *out* of scope, because that decision is invisible from the file tree alone. Point at `AGENTS.md` for the full conventions.

---

## Start here

The umbrella concepts a new reader should open first — usually the broadest "what is X" articles that everything else hangs off of.

- [[concept-id-1]] — short hook explaining why this is the entry point
- [[concept-id-2]] — short hook

---

## Concepts by topic

Group the concept articles the way a reader would naturally look for them. A table tends to read better than a flat list once you have more than a handful, because it lets you show one disambiguating fact per entry.

<!--
The two-column "Concept | Short description" schema below is the default and fits
most wikis. If your corpus needs something different — a Sources column, a
cross-source "Key distinction" column for a comparative wiki, or a richer source
table (Scope indexed / Chapter | Covers / Topic | Year) — pick the schema
deliberately at bootstrap and record it in AGENTS.md. Retrofitting a column across
a large hand-maintained portal is painful. See the skill's
references/index_schema_design.md for the full decision guide and worked examples.
-->

| Concept | Short description |
|---|---|
| [[concept-id-3]] | one-line description |
| [[concept-id-4]] | one-line description |

(Add more sections like this — "## Concepts by [other axis]" — if a single grouping doesn't capture how the wiki is actually used. For example, a research wiki might group by both topic *and* by historical era.)

---

## Sources

(remove if empty) The peer-reviewed papers, datasets, or other primary materials catalogued in `sources/`. This is a navigation aid; the source files themselves are the source of truth.

| Source file | Topic |
|---|---|
| `sources/firstauthor-year-shortslug.md` | one-line topic |

---

## Frontier (red links)

(remove if empty) Concept ids that are referenced from existing articles but do not yet have their own pages. These are listed in `indices/orphans.json` and represent the natural next things to write. Pulling them up here makes the wiki's growth edge visible.

- `concept-id-not-yet-written` — referenced from [[existing-concept]]

---

## About this wiki

- **Conventions and scope**: see `AGENTS.md` at the wiki root
- **Maintenance scripts**: `scripts/build_alias_index.py`, `scripts/build_backlinks.py`, `scripts/check_links.py` (run in that order after any non-trivial edit)
- **Generated indices** (do not hand-edit): `indices/aliases.json`, `indices/backlinks.json`, `indices/orphans.json`
- **Raw source files**: `raw/`
