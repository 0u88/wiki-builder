---
id: front-door-back-door-criteria
title: Front-Door and Back-Door Criteria
aliases: [front-door criterion, back-door criterion, front-door and back-door criteria, back-door adjustment, front-door adjustment]
tags: [causal, identifiability]
status: draft
created: 2026-07-09
updated: 2026-07-09
sources: [robertson-2025-dopfn, balazadeh-2025-causalpfn]
---

**The front-door and back-door criteria** are Pearl's graphical rules for identifying a causal effect from observational data: the back-door criterion licenses adjusting for a set of covariates that blocks all confounding paths, while the front-door criterion identifies an effect through a fully mediating variable even when a confounder is unobserved. In the causal-PFN literature they appear as the *behaviours a model must reproduce*: [[do-pfn]] is shown to "correctly perform the appropriate form of adjustment without explicit knowledge of the causal graph… as if applying the front-door and back-door criteria"[^1]. [[causalpfn]] by contrast is limited to back-door / [[strong-ignorability|ignorability]] adjustment and does not cover the front-door criterion[^2].

## As test cases for Do-PFN

Do-PFN's evaluation is built around six synthetic case studies, each demanding a different adjustment: Observed Confounder, Observed Mediator, Confounder+Mediator, Unobserved Confounder, Front-Door Criterion, and Back-Door Criterion[^1]. The point of this design is that the *correct* estimator differs by scenario — naive adjustment is right in some and disastrously wrong in others — and Do-PFN must infer which regime it is in purely from the observational data, since it is never given the graph[^3]. The Front-Door case is the demanding one: it requires recovering the effect through a mediator despite an unobserved confounder, which simple back-door adjustment cannot do.

## Scope in CausalPFN

CausalPFN's identification story runs entirely through [[strong-ignorability]] (equivalently, back-door adjustment on the covariates), which its [[synthetic-data-prior]] satisfies by construction[^2]. The paper explicitly lists extending beyond ignorability / back-door — to instrumental variables and richer settings — as future work, and does not treat the front-door criterion[^4]. So among the two models, front-door adjustment is a Do-PFN capability, not a CausalPFN one.

## Relationship to other concepts

The two criteria are the classical counterpart to what [[amortized-causal-inference]] must learn implicitly; they rest on [[structural-causal-models]] and the notion of [[strong-ignorability]], and which effects they can identify is bounded by [[observational-equivalence-unidentifiability]].

## Notes

[^1]: [[robertson-2025-dopfn#^front-back-door|Robertson 2025, §front-back-door]]
[^2]: [[balazadeh-2025-causalpfn#^asm-ignorability|Balazadeh 2025, §asm-ignorability]]
[^3]: [[robertson-2025-dopfn#^def-dopfn|Robertson 2025, §def-dopfn]]
[^4]: [[balazadeh-2025-causalpfn#^limitations|Balazadeh 2025, §limitations]]
