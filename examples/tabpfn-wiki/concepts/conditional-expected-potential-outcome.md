---
id: conditional-expected-potential-outcome
title: Conditional Expected Potential Outcome (CEPO)
aliases: [CEPO, conditional expected potential outcome, conditional expected potential outcomes]
tags: [causal, treatment-effect]
status: draft
created: 2026-07-09
updated: 2026-07-09
sources: [balazadeh-2025-causalpfn, robertson-2025-dopfn]
---

**The conditional expected potential outcome (CEPO)** is the estimand $\mu_t(x) := \mathbb{E}[Y_t \mid X = x]$ — the expected outcome under treatment $t$ for units with covariates $x$, in the potential-outcomes framework[^1]. It is the primary target of [[causalpfn]], from which the average treatment effect $\mathrm{ATE} = \mathbb{E}[\mu_1(X) - \mu_0(X)]$ and the conditional average treatment effect $\mathrm{CATE}(x) = \mu_1(x) - \mu_0(x)$ follow directly[^1]. The CEPO is an *expectation*, which distinguishes it from the full [[conditional-interventional-distribution]] that [[do-pfn]] targets.

## Definition

Working in the potential-outcomes framework, CausalPFN targets $\mathbb{E}[Y_t \mid X]$, deliberately removing the aleatoric outcome noise so as to isolate epistemic uncertainty about the effect[^2]. The three "causal effects" it reports — CEPO, CATE, and ATE — are all functionals of $\mu_t$[^1]. This is a modeling choice, not a necessity: [[do-pfn]] instead predicts the entire distribution $p(y \mid \mathrm{do}(t), x)$, from which $\mathbb{E}[y \mid \mathrm{do}(t), x]$ (the same conditional expected potential outcome, though Do-PFN does not use the acronym) can be recovered as a difference of expectations to form CATE[^3].

## Estimating it as a posterior predictive

CausalPFN does not output a point estimate but a **CEPO posterior predictive distribution (CEPO-PPD)**: the distribution of $\mu_t(x)$ obtained by pushing the implicit posterior over data-generating processes through $\mu_t(x;\theta)$[^4]. A concentrated CEPO-PPD means the observational data is informative about the effect; a wide one signals [[observational-equivalence-unidentifiability|epistemic uncertainty]][^4]. This is the causal analogue of the ordinary [[posterior-predictive-distribution]] that [[prior-data-fitted-networks|PFNs]] approximate.

## When it is recoverable

Because $\mu_t$ is only estimable if it is a functional of the observational distribution, CausalPFN's consistency result holds *if and only if* the prior is [[observational-equivalence-unidentifiability|CEPO-identifiable]][^5]. The paper secures this by building [[strong-ignorability]] into its [[synthetic-data-prior]][^6].

## Relationship to other concepts

The CEPO is the expectation-level counterpart of the [[conditional-interventional-distribution]]; its estimation feeds [[heterogeneity-control|CATE]] and ATE, requires [[strong-ignorability]] for identification, and is emitted through a [[histogram-loss-quantized-distribution|quantized output distribution]].

## Notes

[^1]: [[balazadeh-2025-causalpfn#^def-cepo|Balazadeh 2025, §def-cepo]]
[^2]: [[balazadeh-2025-causalpfn#^potential-outcomes|Balazadeh 2025, §potential-outcomes]]
[^3]: [[robertson-2025-dopfn#^cate-from-cid|Robertson 2025, §cate-from-cid]]
[^4]: [[balazadeh-2025-causalpfn#^cepo-ppd|Balazadeh 2025, §cepo-ppd]]
[^5]: [[balazadeh-2025-causalpfn#^thm-consistency|Balazadeh 2025, §thm-consistency]]
[^6]: [[balazadeh-2025-causalpfn#^prior-construction|Balazadeh 2025, §prior-construction]]
