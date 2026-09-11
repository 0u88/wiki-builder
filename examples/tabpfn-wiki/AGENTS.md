# AGENTS.md

This file is the first thing an LLM session should read when working in this wiki, and it is the **canonical instructions for any AI agent** operating in this directory — regardless of which tool the agent is running under. Claude Code reads `CLAUDE.md` (a one-line stub routing here); Codex / ChatGPT / Cursor and most other tools read `AGENTS.md`. This file is the single source of truth.

## Domain

This wiki organizes the ideas behind **TabPFN** — a transformer-based *tabular foundation model* that solves small tabular prediction problems in a single forward pass, with no per-dataset training or hyperparameter tuning — and its extension into **amortized causal inference**. It is built from five primary papers: the foundational **Prior-Data Fitted Networks (PFN)** paper (Müller et al. 2022), the original **TabPFN** classifier (Hollmann et al. 2023), the **Nature TabPFN v2** paper (Hollmann et al. 2025), and two 2025 causal PFNs — **Do-PFN** (Robertson et al. 2025, NeurIPS) and **CausalPFN** (Balazadeh et al. 2025). Scope is the conceptual machinery of these papers: PFNs, in-context learning, the posterior predictive distribution, synthetic-data priors (SCMs, BNNs), the 2D table transformer, foundation-model abilities, and — for the causal papers — amortized estimation of interventional/potential-outcome quantities, the identification assumptions they rely on, and how they are trained and evaluated. Out of scope: general deep-learning and classical causal-inference background except where a source paper directly states or uses it, competing systems except where a paper compares against them, and application case studies not in the five sources.

## Wiki retrieval protocol

When answering questions about topics in this wiki, follow this lookup order:

1. **Re-read this file (`AGENTS.md`)** for the domain, tag vocabulary, source-id conventions, and scope exclusions.
2. **Check `index.md`** at the wiki root for orientation — it is the portal page grouping all concepts and sources.
3. **Check `indices/aliases.json`** to resolve concept names — concepts often have multiple aliases (e.g. `PFN` → `prior-data-fitted-networks`).
4. **Use `indices/backlinks.json`** to find which concepts reference a given concept, and `indices/orphans.json` for red-link frontier concepts.
5. **Read the relevant `concepts/` and `sources/` files** — every non-trivial claim in a concept article has a footnote citation traceable to a specific anchor in a source file.
6. **Ground all answers in `sources/`** — do not answer from training data alone. If the wiki does not cover a topic, say so explicitly rather than generating an uncited answer.

## Boundary discipline

This wiki is the knowledge boundary for questions asked in this directory. If a topic is not covered by concept or source files here, respond with "this wiki does not cover that topic" rather than answering from general knowledge. TabPFN is well-represented in LLM training data, so this discipline matters more than usual: prefer citing a source anchor over recalling a fact. If asked to show the passage behind a citation, open the `sources/` file and quote the actual "Key claims" bullet.

## Tag vocabulary

The controlled list of tags in use. Grep before adding a new tag.

- `pfn` — Prior-Data Fitted Networks and the meta-learning framework
- `tabpfn` — TabPFN-specific model, architecture, and results
- `transformer` — transformer architecture details
- `bayesian` — Bayesian inference, the PPD, priors as distributions over datasets
- `in-context-learning` — learning from context in a forward pass
- `prior` — the synthetic-data prior and its generators (SCMs, BNNs)
- `tabular` — properties and handling specific to tabular data
- `inference` — inference cost, caching, efficiency
- `foundation-model` — foundation-model capabilities and framing
- `causal` — causal inference: interventions, do-operator, potential outcomes, treatment effects
- `identifiability` — identification assumptions and criteria (ignorability, back-door, front-door, unidentifiability)
- `treatment-effect` — CATE/ATE estimands, heterogeneity, and meta-learner/DML baselines
- `evaluation` — metrics and evaluation protocols (coverage/ICE, RCT simulation, OOD robustness)

## Source id convention

`lastname-year-shorttitle`. The five seed sources:

- `muller-2022-pfn` — Müller et al., "Transformers Can Do Bayesian Inference"
- `hollmann-2023-tabpfn` — Hollmann et al., original TabPFN (ICLR 2023)
- `hollmann-2025-tabpfn-nature` — Hollmann et al., TabPFN v2 (Nature 2025)
- `robertson-2025-dopfn` — Robertson et al., "Do-PFN: In-Context Learning for Causal Effect Estimation" (NeurIPS 2025)
- `balazadeh-2025-causalpfn` — Balazadeh et al., "CausalPFN: Amortized Causal Effect Estimation via In-Context Learning" (2025, arXiv:2506.07918)

## Project-specific conventions

- Concept articles synthesize *across* the papers; source files only index a single paper. When a claim differs between TabPFN v1 (2023) and v2 (2025), or between the two causal PFNs (CausalPFN vs Do-PFN), attribute each explicitly.
- Classical causal-inference concepts (ignorability, back-door/front-door, DML, meta-learners) are in scope only as the causal papers state or use them — cite the CausalPFN/Do-PFN anchors, not textbook knowledge. If a needed identification result is only assumed by a paper, keep the article to what the paper says and mark it `status: stub`.
- All math in LaTeX inside `$...$` / `$$...$$` — never Unicode math. Reference style: Wasserman, *All of Statistics*.
- `status: stable` requires the claim to be backed by at least one precise source anchor; `draft` is the default for a well-developed article; `stub` for a lead + minimal body.

## Wikilink policy

When writing or updating a concept article, if a related concept SHOULD exist in this wiki but does not yet have an article, link to it anyway using `[[concept-id]]`. Red links are a feature — they mark the wiki's growth frontier and feed the automated build queue.

A good concept article should produce 3–8 outbound wikilinks, of which at least 2–3 may be red links to concepts not yet written. If you finish writing a concept and it has zero red links, you are probably being too conservative.

Do NOT avoid red links to "keep things clean." A wiki with no red links is a wiki that has stopped growing.

## After any edit

Run in order (requires Python 3):

```
python scripts/build_alias_index.py .
python scripts/build_backlinks.py .
python scripts/check_links.py .
python scripts/unused_claims.py .
```

A non-zero exit from `check_links.py` almost always means a hallucinated citation. Fix it before moving on. `unused_claims.py` surfaces source anchors not yet cited by any concept article — the supply-side growth queue.

## Status

- **Started**: 2026-07-06
- **Last audit**: 2026-07-09 — added the causal cluster (CausalPFN, Do-PFN) and concepts 13–24
- **Size**: 24 concepts, 5 sources
