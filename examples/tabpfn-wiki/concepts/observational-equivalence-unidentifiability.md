---
id: observational-equivalence-unidentifiability
title: Observational Equivalence and Unidentifiability
aliases: [observational equivalence, unidentifiability, CEPO-identifiability, identifiability, observational quotient space]
tags: [causal, identifiability]
status: draft
created: 2026-07-09
updated: 2026-07-09
sources: [balazadeh-2025-causalpfn, robertson-2025-dopfn]
---

**Observational equivalence** is the situation where two different data-generating processes induce the *same* observational distribution $P_{\mathrm{obs}}$ yet imply *different* causal effects; when this happens the effect is **unidentifiable** — no amount of observational data can pin it down[^1]. This is the central obstacle for [[amortized-causal-inference]], and the two causal PFNs handle it in opposite ways: [[causalpfn]] rules it out by making its prior identifiable, while [[do-pfn]] embraces it, treating the spread over an equivalence class as a distinct source of uncertainty[^2].

## The core problem

CausalPFN formalizes this as **CEPO-identifiability**: the [[conditional-expected-potential-outcome|CEPO]] $\mu_t$ is identifiable only when it can be written as a functional of the observational distribution $P_{\mathrm{obs}}$; since different processes can share $P_{\mathrm{obs}}$ but differ in their effects, estimation is impossible without identifiability[^1]. Its consistency guarantee (Proposition 1) is therefore an *if and only if*: the CEPO posterior predictive converges to the true effect precisely when the prior is CEPO-identifiable, proved over an "observational quotient space" of processes sharing $P_{\mathrm{obs}}$ using Doob's consistency theorem[^3]. CausalPFN secures the condition by building [[strong-ignorability]] into the prior[^4].

## Unidentifiability as uncertainty

Do-PFN does not assume identifiability, so it must represent the ambiguity. Its posterior predictive decomposes into three uncertainty sources: aleatoric (the [[structural-causal-models|SCM]] noise), **unidentifiability** — the distribution over observationally equivalent SCMs within an equivalence class — and epistemic — uncertainty about which Markov-equivalence class the finite data belongs to[^5]. Its consistency result (Proposition 3) is correspondingly weaker but honest: as data grows the epistemic term vanishes and the posterior concentrates on the observational-equivalence class $[\theta_0]$, collapsing to the true effect only if $\theta_0$ is identifiable[^6].

## Why it decides the head-to-head

This distinction explains the empirical gap: CausalPFN beats Do-PFN on all four shared benchmarks, and the stated reason is that Do-PFN "does not explicitly enforce identifiability" — its prior can contain observationally equivalent processes, so per the consistency theorem its posterior cannot in general concentrate on the true effect[^7]. The flip side is that on genuinely unidentifiable problems (e.g. an unobserved confounder), Do-PFN's wider uncertainty is the *correct* answer, whereas an identifiability-assuming model would be confidently wrong[^8].

## Relationship to other concepts

Identifiability is what makes [[conditional-expected-potential-outcome|CEPO]] and [[conditional-interventional-distribution|CID]] estimation well-posed; it is secured by [[strong-ignorability]] or the [[front-door-back-door-criteria|adjustment criteria]], and its failure is surfaced through calibrated uncertainty (see [[integrated-coverage-error]]).

## Notes

[^1]: [[balazadeh-2025-causalpfn#^cepo-identifiability|Balazadeh 2025, §cepo-identifiability]]
[^2]: [[robertson-2025-dopfn#^uncertainty-decomp|Robertson 2025, §uncertainty-decomp]]
[^3]: [[balazadeh-2025-causalpfn#^thm-consistency|Balazadeh 2025, §thm-consistency]]
[^4]: [[balazadeh-2025-causalpfn#^prior-construction|Balazadeh 2025, §prior-construction]]
[^5]: [[robertson-2025-dopfn#^uncertainty-decomp|Robertson 2025, §uncertainty-decomp]]
[^6]: [[robertson-2025-dopfn#^thm-consistency|Robertson 2025, §thm-consistency]]
[^7]: [[balazadeh-2025-causalpfn#^vs-dopfn|Balazadeh 2025, §vs-dopfn]]
[^8]: [[robertson-2025-dopfn#^calibration-picp|Robertson 2025, §calibration-picp]]
