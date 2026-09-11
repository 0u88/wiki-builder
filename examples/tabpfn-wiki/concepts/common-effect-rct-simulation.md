---
id: common-effect-rct-simulation
title: Common Effect and RCT Simulation
aliases: [common effect, RCT simulation, randomized controlled trial simulation, common-effect case study]
tags: [causal, evaluation, prior]
status: draft
created: 2026-07-09
updated: 2026-07-09
sources: [robertson-2025-dopfn, balazadeh-2025-causalpfn]
---

**RCT simulation** is the use of a randomized-controlled-trial setup — where treatment is assigned independently of the covariates — as a controlled test bed (and prior ingredient) for causal estimation. In an RCT there is no confounding, so the effect is trivially identified and simple estimators suffice; that makes it a useful *floor* against which to judge whether a causal PFN's extra machinery is buying anything. [[do-pfn]] realizes this as its "Common-Effect" case study, explicitly framed as an RCT[^1], while [[causalpfn]] bakes randomized treatments into its [[synthetic-data-prior]] and validates on real marketing RCTs[^2].

## Do-PFN's Common-Effect case

Do-PFN includes a "Common-Effect" scenario that "perfectly represents a randomized controlled trial (RCT)"[^1]. Its diagnostic value is precisely that here standard tabular regressors — [[tabpfn]] v2 and Random Forest — match Do-PFN, because with no directed edge from treatment to covariates there is no distribution shift between the observational context and the interventional query[^1]. In other words, when the problem is an RCT, causal-specific modeling is unnecessary; Do-PFN's advantage only appears once confounding or mediation is present (see [[front-door-back-door-criteria]]).

## RCTs in CausalPFN

CausalPFN uses RCT structure in two places. In the prior, "Randomized treatments (RCT)" is one of three treatment-logit mechanisms — a constant logit giving uniform propensities, so treatment is independent of covariates[^2]. In evaluation, it uses five real marketing RCTs whose Qini curves yield unbiased top-quantile ATE estimates as ground truth[^2]. Including randomized designs in the prior ensures the model has seen the [[strong-ignorability|no-confounding]] extreme, complementing the confounded and low-overlap regimes produced by [[heterogeneity-control|heterogeneity and positivity controls]].

## Relationship to other concepts

RCT simulation is the unconfounded corner of the [[synthetic-data-prior]] and a real-data validation strategy; it anchors the easy end of the spectrum that [[strong-ignorability]] describes and that the [[front-door-back-door-criteria|adjustment criteria]] generalize away from.

## Notes

[^1]: [[robertson-2025-dopfn#^common-effect-rct|Robertson 2025, §common-effect-rct]]
[^2]: [[balazadeh-2025-causalpfn#^rct-mechanism|Balazadeh 2025, §rct-mechanism]]
