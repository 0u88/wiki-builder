---
id: integrated-coverage-error
title: Integrated Coverage Error (ICE)
aliases: [ICE, integrated coverage error]
tags: [causal, evaluation, calibration]
status: draft
created: 2026-07-09
updated: 2026-07-09
sources: [balazadeh-2025-causalpfn, robertson-2025-dopfn]
---

**Integrated coverage error (ICE)** is a scalar calibration metric introduced by [[causalpfn]] that measures, integrated over all nominal levels, how far a model's credible-interval coverage deviates from its stated level[^1]. For a regression target it is $\mathrm{ICE}_\mu := \int_0^1 (\mathrm{cov}_\mu(\alpha) - \alpha)\, d\alpha$, with a CATE version $\mathrm{ICE}_\tau$; negative values mean the intervals are overconfident[^1]. ICE matters because a causal estimate is only actionable if its uncertainty is trustworthy, and ICE gives a single number for that — but note it is specific to CausalPFN; [[do-pfn]] reports calibration differently, via Prediction Interval Coverage Probability (PICP)[^2].

## Definition and the key inequality

$\mathrm{cov}(\alpha)$ is the empirical probability that the true value falls in the model's level-$\alpha$ interval; perfect calibration gives $\mathrm{cov}(\alpha) = \alpha$ and $\mathrm{ICE} = 0$[^1]. CausalPFN observes an ordering that holds across all model–DGP pairs: $\mathrm{ICE}_\mu \le \mathrm{ICE}_\tau$ — regression coverage sits at or below CATE coverage[^1]. This is practically useful because $\mathrm{ICE}_\tau$ requires the unobservable true CATE, whereas $\mathrm{ICE}_\mu$ is computable from ordinary observational $(t, x, y)$ triples.

## Calibrating with observable quantities

The inequality turns a hidden target into a tunable one: temperature-scaling the output logits to drive the computable $\mathrm{ICE}_\mu \to 0$ (via 5-fold grid search) also calibrates, or makes conservative, the CATE intervals whose error cannot be measured directly[^1]. This same recipe is what rescues calibration [[ood-robustness|out of distribution]]: CausalPFN is severely overconfident on OOD data-generating processes, but regression-ICE temperature scaling removes the overconfidence even there[^3].

## Contrast with Do-PFN's PICP

Do-PFN does not use ICE. Its calibration is assessed with PICP curves, and it is found well-calibrated overall — slightly under-confident on identifiable cases (attributed to [[histogram-loss-quantized-distribution|bar-distribution]] discretization error) and correctly widening on the unidentifiable unobserved-confounder case[^2]. So while both models care about calibrated causal uncertainty, ICE is CausalPFN's instrument and PICP is Do-PFN's.

## Relationship to other concepts

ICE quantifies whether the [[conditional-expected-potential-outcome|CEPO]] posterior predictive is trustworthy; it is tightly coupled to [[ood-robustness]] (via temperature scaling) and to the [[observational-equivalence-unidentifiability|unidentifiability]] that should manifest as wider, still-calibrated intervals.

## Notes

[^1]: [[balazadeh-2025-causalpfn#^metric-ice|Balazadeh 2025, §metric-ice]]
[^2]: [[robertson-2025-dopfn#^calibration-picp|Robertson 2025, §calibration-picp]]
[^3]: [[balazadeh-2025-causalpfn#^ood-calibration|Balazadeh 2025, §ood-calibration]]
