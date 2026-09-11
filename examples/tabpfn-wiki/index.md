# TabPFN Wiki

A personal knowledge base on **TabPFN** — a transformer-based *tabular foundation model* that solves small tabular prediction problems in a single forward pass, with no per-dataset training or hyperparameter tuning — and its extension into **amortized causal inference**. Built from five primary papers: the foundational Prior-Data Fitted Networks paper (Müller et al. 2022), the original TabPFN classifier (Hollmann et al. 2023), the Nature TabPFN v2 paper (Hollmann et al. 2025), and two 2025 causal PFNs — Do-PFN (Robertson et al. 2025) and CausalPFN (Balazadeh et al. 2025). Scope is the conceptual machinery of these papers; general deep-learning and classical causal-inference background is out of scope except where a source paper uses it. See `AGENTS.md` for full conventions.

---

## Start here

- [[prior-data-fitted-networks]] — the framework everything hangs off: transformers trained to do Bayesian prediction by learning from sampled datasets.
- [[in-context-learning]] — the inference mechanism: the whole training set becomes the model's context, no gradient descent at prediction time.
- [[tabular-foundation-model]] — what it all adds up to: one pre-trained network applied to any table, with abilities beyond prediction.
- [[amortized-causal-inference]] — the causal turn: train once on simulated datasets, estimate causal effects on new data in a forward pass (Do-PFN, CausalPFN).

---

## Concepts by topic

**The Bayesian core** — what TabPFN computes and why it is principled.

| Concept | Short description |
|---|---|
| [[prior-data-fitted-networks]] | Transformers trained on sampled datasets to approximate Bayesian prediction |
| [[in-context-learning]] | Learning from the training set given as input, in one forward pass |
| [[posterior-predictive-distribution]] | The Bayesian prediction target a PFN approximates directly |

**The prior** — the synthetic world TabPFN is pre-trained on, its entire inductive bias.

| Concept | Short description |
|---|---|
| [[synthetic-data-prior]] | The distribution over whole datasets used for offline training |
| [[structural-causal-models]] | Causal-graph generators, the backbone of TabPFN v2's prior |
| [[bayesian-neural-networks]] | Weight-space priors; a data generator and an approximation target |
| [[occams-razor]] | The deliberate bias toward simple data-generating structures |

**The tabular model** — architecture and the messiness of real tables.

| Concept | Short description |
|---|---|
| [[2d-transformer-architecture]] | Cell-wise, two-way attention over samples and features |
| [[handling-tabular-peculiarities]] | Missing values, categoricals, scale, uninformative features, outliers |

**Practical payoff** — why it is fast and usable.

| Concept | Short description |
|---|---|
| [[zero-hyperparameter-tuning]] | Strong predictions out of the box, no cross-validation |
| [[state-caching-inference]] | Caching the training-set representation for cheap repeated queries |
| [[tabular-foundation-model]] | Headline results plus density estimation, generation, embeddings, fine-tuning |

**Causal PFNs — the estimands** — what the causal models actually predict (Do-PFN vs CausalPFN).

| Concept | Short description |
|---|---|
| [[amortized-causal-inference]] | Train once on simulated datasets; estimate causal effects in a forward pass |
| [[conditional-interventional-distribution]] | $p(y\mid\mathrm{do}(t),x)$ — Do-PFN's full interventional distribution |
| [[conditional-expected-potential-outcome]] | $\mathbb{E}[Y_t\mid X]$ — CausalPFN's expectation-level estimand |
| [[heterogeneity-control]] | Tuning CATE variance in the prior while preserving the ATE |

**Causal PFNs — identification and assumptions** — when a causal effect can be recovered at all.

| Concept | Short description |
|---|---|
| [[strong-ignorability]] | Unconfoundedness + positivity; CausalPFN enforces it, Do-PFN relaxes it |
| [[observational-equivalence-unidentifiability]] | When different processes share a distribution but differ in effect |
| [[front-door-back-door-criteria]] | Pearl's adjustment rules; Do-PFN reproduces both, CausalPFN only back-door |
| [[double-machine-learning-metalearners]] | DML and S/T/X-Learners — the per-dataset baselines |

**Causal PFNs — training, output and evaluation** — how they are built and judged.

| Concept | Short description |
|---|---|
| [[histogram-loss-quantized-distribution]] | Discretized output distribution / bar-distribution head |
| [[integrated-coverage-error]] | CausalPFN's calibration metric (vs Do-PFN's PICP) |
| [[ood-robustness]] | Behaviour when the test process leaves the prior's support |
| [[common-effect-rct-simulation]] | RCT setups as a prior ingredient and an evaluation floor |

---

## Sources

The five primary papers catalogued in `sources/`. The source files are the ground truth; every concept claim cites an anchor in one of them.

| Source | Topic | Year |
|---|---|---|
| `sources/muller-2022-pfn.md` | Prior-Data Fitted Networks; transformers approximate Bayesian inference | 2022 |
| `sources/hollmann-2023-tabpfn.md` | Original TabPFN classifier for small tables (ICLR) | 2023 |
| `sources/hollmann-2025-tabpfn-nature.md` | TabPFN v2, a tabular foundation model (Nature) | 2025 |
| `sources/robertson-2025-dopfn.md` | Do-PFN: in-context estimation of interventional distributions (NeurIPS) | 2025 |
| `sources/balazadeh-2025-causalpfn.md` | CausalPFN: amortized causal effect estimation via ICL (NeurIPS) | 2025 |

---

## Frontier (red links)

Concepts referenced from existing articles but not yet written — the natural next things to add (see `indices/orphans.json`).

- `tabpfn` — the model itself as a hub article; referenced from nearly every concept
- `gaussian-process` — the tractable-PPD benchmark PFNs were first validated against
- `riemann-distribution` — the discretized regression output head, ancestor of the causal histogram loss
- `permutation-invariance` — why the training set is treated as an unordered set
- `do-pfn` — model hub for the interventional-distribution causal PFN (Robertson et al. 2025)
- `causalpfn` — model hub for the potential-outcome causal PFN (Balazadeh et al. 2025)

---

## About this wiki

- **Conventions and scope**: see `AGENTS.md` at the wiki root
- **Maintenance scripts**: `scripts/build_alias_index.py`, `scripts/build_backlinks.py`, `scripts/check_links.py`, `scripts/unused_claims.py` (run in that order after any non-trivial edit)
- **Generated indices** (do not hand-edit): `indices/aliases.json`, `indices/backlinks.json`, `indices/orphans.json`, `indices/unused_claims.json`
- **Raw source PDFs**: `raw/`
