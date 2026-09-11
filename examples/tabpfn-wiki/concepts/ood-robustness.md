---
id: ood-robustness
title: OOD Robustness to Noise and Non-Linearity
aliases: [OOD robustness, out-of-distribution robustness, robustness to noise and non-linearity]
tags: [causal, evaluation]
status: draft
created: 2026-07-09
updated: 2026-07-09
sources: [robertson-2025-dopfn, balazadeh-2025-causalpfn]
---

**Out-of-distribution (OOD) robustness** for a causal PFN is how well it holds up when the test data-generating process falls outside the [[synthetic-data-prior]] it was trained on — different noise distributions, stronger non-linearities, or larger causal graphs. Because a PFN's entire competence is inherited from its prior, OOD behaviour is the sharpest test of whether it has learned a general estimation procedure or merely memorized its training distribution. [[do-pfn]] and [[causalpfn]] report contrasting OOD profiles: Do-PFN degrades gracefully on many shifts[^1], while CausalPFN is well-calibrated in-distribution but severely overconfident OOD unless recalibrated[^2].

## Do-PFN under distribution shift

Do-PFN is robust to unseen *noise* distributions — Laplace, Student-T, Gumbel, and mixtures — and to different non-linearities and post-nonlinearities not in its training prior[^1]. Its failure modes are specific: performance drops sharply when the Gaussian noise variance is doubled beyond the training range, and on the pointwise average of training functions[^1]. Graph size is a version story: v1 degrades on large graphs (21–50 nodes) while v1.1, trained on graphs up to 60 nodes, recovers — a direct illustration that widening the prior fixes the corresponding OOD gap[^1].

## CausalPFN and recalibration

CausalPFN's OOD study uses synthetic polynomial (degrees 1–4) and sinusoidal data-generating families with Gaussian, Laplace, and Uniform noise[^2]. In-distribution it is calibrated or conservative, but on DGPs outside its prior support it becomes severely overconfident — its intervals are too narrow[^2]. The fix reuses its calibration machinery: temperature-scaling the logits to drive the observable regression [[integrated-coverage-error|ICE]] to zero removes the overconfidence even out of distribution[^2]. So CausalPFN's OOD robustness is achieved not by the base model but by a cheap post-hoc recalibration step.

## The shared lesson

Both results point to the same principle behind [[amortized-causal-inference]]: a PFN generalizes exactly as far as its prior stretches, and honest uncertainty (or explicit recalibration) is what keeps it safe past that edge. This mirrors how the original [[tabular-foundation-model]] handles distribution peculiarities by generating them in the prior.

## Relationship to other concepts

OOD robustness stresses the coverage of the [[synthetic-data-prior]]; it is measured through calibration ([[integrated-coverage-error|ICE]] / PICP) and is bounded by the same [[observational-equivalence-unidentifiability|identifiability]] limits that govern in-distribution estimation.

## Notes

[^1]: [[robertson-2025-dopfn#^ood-robustness|Robertson 2025, §ood-robustness]]
[^2]: [[balazadeh-2025-causalpfn#^ood-calibration|Balazadeh 2025, §ood-calibration]]
