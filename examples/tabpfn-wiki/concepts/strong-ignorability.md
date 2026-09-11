---
id: strong-ignorability
title: Strong Ignorability and Unconfoundedness
aliases: [strong ignorability, unconfoundedness, ignorability, no unmeasured confounding]
tags: [causal, identifiability]
status: draft
created: 2026-07-09
updated: 2026-07-09
sources: [balazadeh-2025-causalpfn, robertson-2025-dopfn]
---

**Strong ignorability** is the standard assumption under which a treatment effect can be identified from observational data: that treatment assignment is, conditional on the covariates, independent of the potential outcomes (unconfoundedness) and that every unit has a nonzero chance of each treatment (positivity)[^1]. It is the central identifying assumption of [[causalpfn]], which even builds it into its [[synthetic-data-prior]] by construction[^2]. [[do-pfn]] takes the opposite stance: it deliberately targets scenarios *without* unconfoundedness[^3], making this assumption the sharpest axis of contrast between the two causal PFNs.

## The assumption

CausalPFN's Assumption 1 states strong ignorability as (i) $Y_t \perp T \mid X$ for all $t$ (unconfoundedness / no unmeasured confounding) and (ii) $P(T = t \mid X) > 0$ almost everywhere (positivity / overlap)[^1]. Both parts are needed: unconfoundedness makes the [[conditional-expected-potential-outcome|CEPO]] a functional of the observational distribution, and positivity ensures every covariate stratum contains both treated and untreated units. The paper stresses that ignorability is untestable in practice — no data can confirm the absence of a hidden confounder[^4].

## Ignorability by construction

Because CausalPFN learns from simulated data-generating processes, it can *guarantee* ignorability in its prior: treatment $T$ is drawn as $T \sim \mathrm{Bernoulli}(\mathrm{Sigmoid}(f(X)))$ with logits $f$ depending only on the covariates $X$, so $T$ is unconfounded given $X$ by design, and the sigmoid guarantees positivity[^2]. This is what makes the prior [[observational-equivalence-unidentifiability|CEPO-identifiable]] and is the reason CausalPFN's consistency guarantee holds[^5].

## Relaxing it

Do-PFN argues that positing a prior over [[structural-causal-models|SCMs]] — hence over causal graphs — extends classical do-calculus, which fixes a single graph, and so "also includes scenarios without the unconfoundedness assumption"[^3]. Its synthetic case studies include an Unobserved-Confounder setting, where it correctly widens its uncertainty rather than returning a falsely confident effect[^6]. The trade-off surfaces in the head-to-head: on benchmarks that *do* satisfy ignorability, CausalPFN beats Do-PFN, which the authors attribute to CausalPFN enforcing identifiability while Do-PFN does not[^7].

## Relationship to other concepts

Strong ignorability is the classic route to [[observational-equivalence-unidentifiability|identifiability]]; it underlies the [[front-door-back-door-criteria|back-door criterion]], is assumed by [[double-machine-learning-metalearners|DML and meta-learners]], holds trivially in the [[common-effect-rct-simulation|randomized (RCT)]] case, and is the dividing line between [[causalpfn]] (enforces it) and [[do-pfn]] (relaxes it).

## Notes

[^1]: [[balazadeh-2025-causalpfn#^asm-ignorability|Balazadeh 2025, §asm-ignorability]]
[^2]: [[balazadeh-2025-causalpfn#^prior-construction|Balazadeh 2025, §prior-construction]]
[^3]: [[robertson-2025-dopfn#^no-unconfoundedness|Robertson 2025, §no-unconfoundedness]]
[^4]: [[balazadeh-2025-causalpfn#^limitations|Balazadeh 2025, §limitations]]
[^5]: [[balazadeh-2025-causalpfn#^thm-consistency|Balazadeh 2025, §thm-consistency]]
[^6]: [[robertson-2025-dopfn#^calibration-picp|Robertson 2025, §calibration-picp]]
[^7]: [[balazadeh-2025-causalpfn#^vs-dopfn|Balazadeh 2025, §vs-dopfn]]
