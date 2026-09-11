# Index table schema design reference

This file is loaded on demand when you are designing (or revising) the concept
and source tables on a wiki's portal page (`index.md`). The short version lives
in `SKILL.md` under "The portal page → Index table schemas"; this file is the
authoritative spec, with worked examples and the reasoning behind each choice.

The portal's two main tables — the concept list and the source list — are plain
markdown tables. Their column schema is **not** fixed across wikis: it should
follow the shape of the material. A schema that fits a two-textbook theory wiki
is wrong for an eleven-paper research wiki, and forcing one shared schema on both
produces empty, padded-looking columns. This file tells you how to pick.

## Contents

- [The governing rule](#the-governing-rule)
- [Concept table](#concept-table)
- [Source table](#source-table)
- [Grouping axis](#grouping-axis)
- [Formatting rules](#formatting-rules)
- [Fix the schema at bootstrap](#fix-the-schema-at-bootstrap)
- [Worked examples](#worked-examples)

## The governing rule

**A column earns its place only if (a) it is filled for most rows and (b) it is
not already carried by frontmatter.**

The second clause matters: `tags`, `aliases`, and `status` all live in each
concept's frontmatter already. Repeating them as portal columns duplicates data
that will drift out of sync — the frontmatter says `status: stable`, the portal
still says `draft`, and now a reader doesn't know which to trust. Keep the portal
to information that is *navigational* (what is this, where do I look) rather than
*metadata* (which is the frontmatter's job).

The first clause is what prevents padded, half-empty tables. A column that is
blank for 70% of rows isn't structure — it's visual noise that makes the table
read as broken. If you can't fill a column for most rows, it doesn't belong.

## Concept table

**Default — two columns.** This is the right starting point for almost every
wiki, and three of the four reference wikis use exactly this:

```markdown
| Concept | Short description |
|---|---|
| [[concept-id]] | one-line gloss — ideally the lead's first sentence, kept under ~20 words |
```

- `Concept` is always a `[[wikilink]]` to the concept article.
- `Short description` is a single line. The lead's first sentence, trimmed, is
  usually the best gloss — it is already written to be self-contained, and reusing
  it keeps the portal and the article consistent. Math is allowed but must be
  LaTeX (`$...$`), like everywhere else in the wiki.

**Optional columns — add at most one, and only on a real trigger:**

| Column | Add it when | How it's filled |
|---|---|---|
| `Sources` | The wiki draws on several overlapping sources and you want per-concept provenance visible at a glance | Derivable from each concept's `sources:` frontmatter — can be filled or regenerated mechanically rather than typed |
| `Key distinction` / `Notes` | The wiki is *comparative* — the same concept is treated differently across sources and that contrast is the point (e.g. a deliberately dual-textbook wiki) | Hand-written editorial judgment; not derivable |

The `Key distinction` column is the one to be most careful with. It is only worth
its width when the wiki was *built to compare* — when a reader's main question is
"how do these two books differ on entropy?" rather than "what is entropy?" On a
wiki where most concepts come from a single source, this column sits empty and
actively misleads, because it implies a cross-source tension that usually isn't
there. Don't add it speculatively.

## Source table

Choose the source-table schema by **corpus type**. This is the dimension along
which the reference wikis correctly diverged, so do not try to unify it:

| Corpus | Schema | Use when |
|---|---|---|
| Few textbooks, whole-book ingestion | `Source file \| Topic` | The filename plus a one-line title is all a reader needs |
| Few textbooks, *partial* ingestion | `Source file \| Scope indexed` | You ingested only some chapters and must record which are authoritative, so no one cites un-ingested material by mistake |
| Chapter-granular ingestion | `Source file \| Chapter \| Covers` | Source files are split one-per-chapter and you want fine-grained "what's where" |
| Paper / mixed corpus | `Source \| Topic \| Year` | Dated primary literature where recency matters; add an `Authors` column only if attribution is load-bearing |

Two refinements worth knowing:

- For a **partial-ingestion** wiki, the `Scope indexed` cell is doing real safety
  work: it is the contract that says "Pearl Chs 1–4, 6 and §7.1.4 are in; the rest
  is not." Without it, a future session has no cheap way to know whether a claim it
  wants to cite is actually backed by an ingested chapter.
- For a **paper/mixed corpus**, split the table into sub-tables when the corpus
  mixes primary and reference material — e.g. a `Source papers` table and a
  separate `Surveys and textbooks` table. The two play different roles (primary
  evidence vs. unifying reference) and readers look for them differently.

## Grouping axis

Pick **one** axis for grouping the concept tables into sections, and record it in
`AGENTS.md` so future sessions stay consistent:

- **By topic / subject** — the safe default for a unified field (e.g. information
  theory grouped into "Core Shannon quantities", "Inequalities", "Coding theorems").
- **By framework / tradition** — when the field has competing paradigms that a
  reader navigates by (e.g. causal inference split into potential-outcomes vs.
  graphical-SCM concepts).
- **By role in a method hierarchy** — core → extensions → foundations →
  cross-cutting (e.g. conformal prediction).

Use the same axis throughout one portal. Mixing axes ("some sections by topic,
some by tradition") makes the portal unpredictable to scan. If a single axis
genuinely doesn't capture how the wiki is used, it is fine to add a *second*
complete grouping further down the page (e.g. "Concepts by topic" and then
"Concepts by era") — but each grouping should be internally consistent.

## Formatting rules

- **Use the compact `|---|---|` delimiter style.** Do not hand-pad cells with
  spaces to align the pipes visually. Padding looks tidy in a frozen snapshot, but
  it breaks the instant a row with a longer cell is added, and the wide runs of
  whitespace read as an empty column to anyone scanning the raw markdown. (This is
  a real failure mode — a padded first table next to compact later tables looks
  like a schema mismatch even when the columns are identical.)
- **Escape pipes inside wikilink display text.** A `[[stem|alias]]` link inside a
  table cell must be written `[[stem\|alias]]`, or the `|` is parsed as a column
  separator and the table row breaks. This is one more reason body citations use
  footnote `[^N]` references, which need no escaping — but concept-to-concept
  wikilinks in portal cells still need the backslash.

## Fix the schema at bootstrap

Decide the concept- and source-table columns *before* writing the first concept,
and record the choice in `AGENTS.md`. Two reasons this matters more than it looks:

1. **The portal is hand-maintained, not generated.** The maintenance scripts
   deliberately don't scan or rebuild `index.md`. So there is no "regenerate from
   frontmatter" escape hatch — adding a column later means hand-editing every
   existing row.
2. **Retrofitting scales badly.** Adding a `Sources` column to a 100-concept
   portal is a hundred manual lookups. Choosing the schema up front costs nothing;
   changing it at 100 concepts is an afternoon.

If you genuinely need to add a column later and the wiki is large, the least-bad
path is to script the extraction (e.g. read every concept's `sources:` frontmatter
to populate a new `Sources` column) rather than doing it by hand — but the column
content still has to be spliced into the hand-maintained table, so it is never as
clean as deciding correctly at bootstrap.

## Worked examples

The four reference wikis, as concrete instances of the rules above:

**Causal inference** — three textbooks, partially ingested, two competing
frameworks.
- Concepts: `Concept | Short description`, grouped **by framework/tradition**
  (potential-outcomes / estimation strategies / graphical-SCM / cross-cutting).
- Sources: `Source file | Scope indexed` — the partial-ingestion schema, because
  only specific chapters of each book are authoritative.

**Information theory** — two textbooks, deliberately compared, chapter-split.
- Concepts: `Concept | Sources | Key distinction between books` — the rare
  three-column comparative schema, because contrasting Cover & Thomas against
  MacKay *is the wiki's reason to exist*. This is the one case where the
  `Key distinction` column is filled for nearly every row.
- Sources: `Source file | Chapter | Covers` — chapter-granular, one row per
  ingested chapter.

**Conformal prediction** — eleven papers plus two references.
- Concepts: `Concept | Short description`, grouped **by role** (core methods /
  extensions / theoretical foundations / cross-cutting).
- Sources: `Source | Topic | Year`, split into a `Source papers` table and a
  separate `Surveys and textbooks` table — the paper/mixed-corpus schema.

**Machine learning theory** — two textbooks, heavily overlapping.
- Concepts: `Concept | Short description`, grouped **by topic** (foundations of
  learnability / complexity measures / algorithms with theory / cross-cutting).
- Sources: `Source file | Topic` — the leanest schema; two whole books, a filename
  and a title line each.

The takeaway: all four share the same *page skeleton* (lead + scope → "Start here"
→ concept tables → source tables → "Frontier" red links → "About this wiki"), but
their *table schemas* diverge along exactly two dimensions — whether concepts need
a cross-source comparison column, and what granularity/recency the source corpus
demands. Match those two dimensions and the schema picks itself.
