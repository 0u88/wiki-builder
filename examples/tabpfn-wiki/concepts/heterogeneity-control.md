---
id: heterogeneity-control
title: Heterogeneity Control
aliases: [heterogeneity control, treatment-effect heterogeneity, CATE heterogeneity, heterogeneity hyperparameter]
tags: [causal, treatment-effect, prior]
status: draft
created: 2026-07-09
updated: 2026-07-09
sources: [balazadeh-2025-causalpfn, robertson-2025-dopfn]
---

**Heterogeneity control** is the deliberate tuning of how much a treatment's effect varies across units — the spread of the conditional average treatment effect (CATE) — when constructing a [[synthetic-data-prior]] for causal estimation. [[causalpfn]] exposes this as an explicit prior hyperparameter so its training distribution spans everything from fully homogeneous effects to strongly heterogeneous ones, without disturbing the average effect[^1]. It matters because a causal PFN can only estimate the range of CATE shapes its prior taught it, so controlling heterogeneity in the prior directly controls what the model can generalize to.

## The mechanism in CausalPFN

CausalPFN draws a heterogeneity hyperparameter $\eta \sim \mathrm{Unif}[0,1]$ that rescales the CATE variance while preserving the ATE: $\mathrm{Var}[\tau \mid x] = \eta^2 \mathrm{Var}[\tau_{\mathrm{raw}} \mid x]$, so $\eta = 0$ gives a fully homogeneous (zero-variance) effect and $\eta = 1$ recovers the original heterogeneity[^1]. A separate parameter $\gamma \in [0,1]$ controls positivity by exacerbating extreme propensities to simulate poor overlap[^1]. Sampling $\eta$ and $\gamma$ across their ranges forces the model to see a broad spectrum of heterogeneity and [[strong-ignorability|overlap]] regimes during pre-training.

## Why it matters for CATE

The conditional average treatment effect $\mathrm{CATE}(x) = \mu_1(x) - \mu_0(x)$ is the quantity that captures *who* benefits from treatment, and estimating it well is the headline task for both causal PFNs — CausalPFN attains the best average CATE rank across 310 benchmark tasks[^2], and Do-PFN's CATE, derived from its [[conditional-interventional-distribution|interventional distribution]], beats meta-learners and DML baselines[^3]. A prior that under-represents heterogeneity would bias a model toward flat, near-ATE predictions; explicit heterogeneity control is how CausalPFN avoids that failure mode.

## Relationship to other concepts

Heterogeneity control is a design knob of the [[synthetic-data-prior]] specific to causal estimation; it governs the [[conditional-expected-potential-outcome|CEPO]]/CATE spread the model learns, and pairs with positivity control to cover the assumptions behind [[double-machine-learning-metalearners|meta-learners]].

## Notes

[^1]: [[balazadeh-2025-causalpfn#^heterogeneity-control|Balazadeh 2025, §heterogeneity-control]]
[^2]: [[balazadeh-2025-causalpfn#^results-table1|Balazadeh 2025, §results-table1]]
[^3]: [[robertson-2025-dopfn#^results|Robertson 2025, §results]]
