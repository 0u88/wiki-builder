---
id: histogram-loss-quantized-distribution
title: Histogram Loss and Quantized Distribution
aliases: [histogram loss, quantized distribution, bar distribution, discretized output distribution]
tags: [causal, evaluation, transformer]
status: draft
created: 2026-07-09
updated: 2026-07-09
sources: [balazadeh-2025-causalpfn, robertson-2025-dopfn]
---

**The histogram loss** trains a network to output a continuous distribution by discretizing the target axis into bins and minimizing cross-entropy against a smoothed one-hot target — turning regression into classification over a **quantized distribution**[^1]. [[causalpfn]] uses it to emit its [[conditional-expected-potential-outcome|CEPO]] posterior predictive, and [[do-pfn]] uses the same family of "bar distribution" to emit its [[conditional-interventional-distribution|interventional distribution]][^2]. This is the causal-PFN inheritance of the [[riemann-distribution]] regression head from the original PFN work, and it is what lets these models report full distributions and calibrated intervals rather than point estimates.

## The CausalPFN construction

CausalPFN discretizes the outcome axis into $L = 1024$ bins over $[-10, 10]$: query tokens are projected to $L$ logits and softmaxed into a quantized distribution, then rescaled to outcome units[^1]. The training target is not a hard bin but the true CEPO smoothed by a narrow Gaussian $\mathcal{N}(\mu_t(x), \sigma^2)$ integrated over the bins, against which cross-entropy is minimized[^1]. The paper shows this histogram loss approximates the causal data-prior loss and coincides with it in the limit $\sigma \to 0$, $L \to \infty$ — so the discretization is a controlled approximation, not an ad-hoc choice[^1].

## The Do-PFN bar distribution

Do-PFN's output is likewise a bar-distribution (a histogram / discretized [[riemann-distribution]]) parameterizing its posterior over interventional outcomes[^2]. The discreteness has a measurable cost: Do-PFN attributes its slight under-confidence on identifiable cases partly to "discretization error resulting from using a bar-distribution to parameterize the posterior"[^3]. So the quantized head is both what enables distributional output and a small source of miscalibration to be managed (see [[integrated-coverage-error]]).

## Why quantize at all

Discretizing sidesteps assuming a parametric outcome family: a histogram can represent skew, multimodality, and heavy tails that a Gaussian head cannot, which matters for the full [[conditional-interventional-distribution]] and for [[ood-robustness|robustness to unusual noise]]. The price is a bin-resolution/accuracy trade-off ($L$ bins) and the discretization error above.

## Relationship to other concepts

The histogram loss is the causal descendant of the [[riemann-distribution]] head; it produces the distributional outputs whose calibration [[integrated-coverage-error|ICE]] and PICP measure, and it is a component of the [[2d-transformer-architecture|transformer]] that both causal PFNs build on.

## Notes

[^1]: [[balazadeh-2025-causalpfn#^loss-histogram|Balazadeh 2025, §loss-histogram]]
[^2]: [[robertson-2025-dopfn#^arch-histogram|Robertson 2025, §arch-histogram]]
[^3]: [[robertson-2025-dopfn#^calibration-picp|Robertson 2025, §calibration-picp]]
