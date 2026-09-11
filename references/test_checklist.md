# Wiki Retrieval Test Checklist

A checklist for stress-testing whether an LLM can actually retrieve and reason over a personal wiki built with `wiki-builder`. Use this whenever you finish a new wiki, restructure an existing one, or change `AGENTS.md`.

The point is not to prove the wiki "works" — easy questions always work. The point is to find the **edge** of where it stops working, so you know what to fix.

---

## Setup

- [ ] Pick the wiki and the AI environment to test (Claude Code is recommended — it most closely matches the real "AI uses file tools to explore" use case)
- [ ] Make sure the indices are up to date: run `build_alias_index.py`, `build_backlinks.py`, and `check_links.py` before testing
- [ ] Have `AGENTS.md` open in another window so you can update it as gaps appear
- [ ] Decide whether to record the AI's exploration trace (which files it reads, in what order) — this is the most valuable output of the test

---

## Tier 1 — Lookup questions (sanity check)

These should all pass. If they don't, something basic is broken (lead-first not followed, frontmatter malformed, etc.).

- [ ] **Single-concept definition**: "What is X?" where X is one of the wiki's main concepts
  - *Pass criterion*: AI reads one file's lead and answers correctly
  - *What it tests*: lead-first design

- [ ] **Source attribution**: "Which paper proposed X?"
  - *Pass criterion*: AI returns the correct source ID from the concept's `sources:` frontmatter
  - *What it tests*: frontmatter as metadata is being read, not just prose

- [ ] **Two-way comparison**: "How does X differ from Y?"
  - *Pass criterion*: AI reads both concept files and produces a structured comparison
  - *What it tests*: basic cross-file synthesis

---

## Tier 2 — Structural questions (stress test)

These probe whether the AI is actually using the wiki's structural features (indices, wikilinks, backlinks) or just doing brute-force grep. **This is where most wikis reveal their weaknesses.**

- [ ] **Multi-source counting**: "How many sources mention X?"
  - *Pass criterion*: AI gets the right count
  - *What to watch*: **Does it use `indices/backlinks.json` or does it grep?** If it greps, your `AGENTS.md` is not telling it about the indices, or the indices weren't built. Grep is fine at small scale but won't survive aliases or 500+ files.

- [ ] **Three-hop traversal**: A question that requires chaining at least three lookups, e.g. "Which sources used method M, and which of those sources are about environment E?"
  - *Pass criterion*: AI correctly follows method → sources → concepts → tag, and answers
  - *What to watch*: where it gets stuck. Most failures happen at the second hop because the AI doesn't realize backlinks can be traversed

- [ ] **Claim-level sourcing**: Pick a specific sentence in a concept article and ask "where does this specific claim come from?"
  - *Pass criterion*: AI returns the source ID **plus** the location anchor (`#thm-1`, `#sec-3.2`, etc.)
  - *What it tests*: whether your inline `[^src:...]` citations are actually granular, or whether you've been writing only frontmatter-level citations

- [ ] **Frontier question**: "Which concepts in this wiki have the fewest sources / are most under-developed?"
  - *Pass criterion*: AI uses `indices/orphans.json` or scans frontmatter to identify stubs
  - *What it tests*: whether the AI knows about the meta-indices and can use them for self-diagnosis of the wiki

---

## Tier 3 — Boundary questions (most important)

These test whether the wiki has actually become the AI's "world boundary," or whether the AI is silently falling back on its training data while pretending to use the wiki. **Run at least one of these in every test session.**

- [ ] **The "I don't know" test**: Ask about something plausibly in-domain but actually absent from the wiki
  - Example: if your wiki is about DAS seismology, ask about a related-but-uncovered topic like "fiber-optic gyroscopes" or "DAS for pipeline monitoring"
  - *Pass criterion*: AI explicitly says the wiki does not cover this, **without** generating a confident answer from its prior knowledge
  - *Failure mode*: AI produces a plausible answer with no citations, or with citations to sources that don't actually discuss the asked topic
  - *What it tests*: the most important property of any retrieval system — knowing what it doesn't know

- [ ] **The contradiction test**: "Are there any places in this wiki where two sources disagree, or where a claim in one concept is challenged by a source cited in another?"
  - *Pass criterion*: AI either finds a real disagreement or correctly reports that it didn't find one after checking
  - *Failure mode*: AI invents a tension that isn't there, or claims everything agrees without actually checking
  - *What it tests*: whether the AI is reading sources critically or just summarizing the most prominent claim in each file

- [ ] **The fabricated-citation test**: After the AI gives an answer with citations, pick one citation and ask "Can you show me the exact passage in `sources/<id>.md` that supports this?"
  - *Pass criterion*: AI quotes a real passage that genuinely supports the claim
  - *Failure mode*: AI confidently quotes a passage that doesn't exist, or quotes a real passage that doesn't actually say what was claimed
  - *What it tests*: whether citations are real or post-hoc decoration

---

## Math notation checks

For any wiki that contains math-heavy concept articles, run these checks after the structural and boundary tiers. Math notation inconsistency is a slow rot — it doesn't break anything immediately, but it degrades readability and signals that the wiki is LLM-generated rather than authored.

- [ ] **Delimiter consistency**: Grep all concept files for `\(`, `\## `, and bare `\begin{align}` (without `aligned`). Any hit is a failure — the wiki uses `$ ... $` for inline, `$$ ... $$` for display, and `\begin{aligned}` inside `$$` for multi-line.
  - Quick check: `grep -rnP '\\\\\\(|\\\\\\)|\\\\begin\{align\}[^e]' concepts/`
  - *Pass criterion*: zero matches

- [ ] **Display math spacing**: Spot-check 3–5 display equations. Each `$$` block must have a blank line above and below it, and must be on its own paragraph (not inline with prose). Fenced equations crammed against prose are the most common formatting error.
  - *Pass criterion*: no display equation has prose on the same line or is missing blank-line separation

- [ ] **Wasserman-style operators**: Grep for common mistakes from the blacklist in `references/math_conventions.md`:
  - `E[` or `E(` without `\mathbb` → should be `\mathbb{E}[`
  - `P(` without `\mathbb` → should be `\mathbb{P}(`
  - `\arg\max` or `\argmax` → should be `\operatorname*{arg\,max}`
  - `^T` or `^{T}` for transpose → should be `^\top`
  - `||` for norms → should be `\|`
  - `KL(` → should be `D_{\mathrm{KL}}(`
  - `\text{` for operator names → should be `\mathrm{` or `\operatorname{}`
  - *Pass criterion*: zero matches for any of these patterns in math contexts

- [ ] **Inline fraction discipline**: Spot-check inline math for `\frac{}{}` usage. Inline `\frac` inflates line height and should be replaced with `/` notation (e.g., `$1/2$` not `$\frac{1}{2}$`). Reserve `\frac` for display math only.
  - *Pass criterion*: no inline `$...\frac{}{}...$` except in rare cases where readability demands it

- [ ] **Vector/matrix boldness**: If the article uses vectors or matrices, verify they use `\mathbf{}` (e.g., `\mathbf{x}`, `\mathbf{A}`). Check that vector *components* are plain italic with subscript (`$x_i$`, not `$\mathbf{x}_i$`). Articles that are purely about probability/measure theory may opt out with a notation note — that's fine.
  - *Pass criterion*: consistent use of bold for vectors/matrices, plain italic for components, within each article

- [ ] **Cross-article consistency**: Pick a symbol that appears in multiple concept articles (e.g., expectation, probability, a loss function) and verify it uses the same notation everywhere. The most common drift: one article uses `\mathbb{E}` while another uses `E` or `\mathrm{E}`.
  - *Pass criterion*: identical notation for the same object across all articles checked

### Classifying math notation failures

| Category | Example | Fix |
|----------|---------|-----|
| **Convention violation** | `\arg\max` instead of `\operatorname*{arg\,max}` | Fix the notation in the article |
| **Renderer incompatibility** | Bare `\begin{align}` that won't render in Obsidian | Replace with `$$\begin{aligned}...\end{aligned}$$` |
| **Cross-article drift** | Article A uses `\mathbb{E}`, article B uses `E[X]` | Standardize to `\mathbb{E}` in both |
| **Spacing/layout error** | Display equation with no blank line above it | Add blank lines around `$$` blocks |

---

## What to record

For each question, jot down:

- [ ] **The exploration trace** — which files the AI opened, in what order. This is more diagnostic than the final answer.
- [ ] **Did it use `indices/`?** Or did it grep / scan directories blindly?
- [ ] **Citation quality** — does the answer cite source IDs that exist? At the granularity of files only, or with `#anchor` location precision?
- [ ] **Confidence calibration** — when the wiki is silent on something, does the AI notice?

---

## After testing

- [ ] List the questions that passed without issue → these are your wiki's strengths
- [ ] List the questions that failed or required AI to work too hard → these are gaps in either content, structure, or `AGENTS.md`
- [ ] For each failure, classify it:
  - **Content gap**: the wiki really doesn't have what's needed → write more concepts/sources
  - **Structural gap**: the information is there but the AI couldn't find it efficiently → add backlinks, fix aliases, add wikilinks
  - **`AGENTS.md` gap**: the structure exists but the AI didn't know to use it → update `AGENTS.md` retrieval playbook
  - **Tooling gap**: a missing index or check would have prevented this → consider a new helper script

- [ ] Re-run the failing questions after fixes to verify improvement

---

## Notes on test cadence

- **First time testing a new wiki**: do all of Tier 1 + at least 2 from each of Tiers 2 and 3. If the wiki has math-heavy articles, run the math notation checks on all of them.
- **After restructuring or `AGENTS.md` changes**: re-run the questions that previously failed, plus 1 boundary question
- **After writing new math-heavy concept articles**: run the math notation checks on the new articles (delimiter consistency, Wasserman operators, cross-article consistency)
- **As the wiki grows past ~100 concepts**: re-run a full Tier 2 round, because grep-based fallbacks that worked at small scale start failing here
- **Quarterly sanity check**: pick 3 random questions across all tiers, see if anything has rotted
