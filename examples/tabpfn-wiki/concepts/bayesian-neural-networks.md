---
id: bayesian-neural-networks
title: Bayesian Neural Networks (BNNs)
aliases: [BNN, BNNs, bayesian neural network, bayesian neural networks]
tags: [prior, bayesian, pfn]
status: draft
created: 2026-07-06
updated: 2026-07-06
sources: [muller-2022-pfn, hollmann-2023-tabpfn, hollmann-2025-tabpfn-nature]
---

**A Bayesian neural network (BNN)** places a prior distribution over a network's weights (and optionally its architecture) instead of fixing them, turning the network into a distribution over functions. In the [[prior-data-fitted-networks|PFN]] line of work, BNNs serve two roles: as a *target* Bayesian model whose intractable [[posterior-predictive-distribution]] a PFN can approximate, and as a *generator* in the [[synthetic-data-prior]] — sampling random weights and features and propagating them forward produces a synthetic dataset[^1]. BNNs were one of the two priors mixed in the original [[tabpfn]], later largely superseded by [[structural-causal-models]].

## BNNs as a data-generating prior

To sample a dataset from a BNN prior, one draws random weights (Xavier-initialized), draws i.i.d. normal feature vectors, and propagates them through the network to obtain targets $y_i = \phi(x_i)$[^1]. The PFN framework can go further and be "fully Bayesian … about the weights of the BNN, [and] its architecture, too," by sampling an architecture $A\sim p(A)$ before the weights and integrating over both in a single inference[^1]. In the 2025 model, "small neural networks" are one of the four edge-mapping types inside the [[structural-causal-models|SCM]] generator, so BNN-style computations survive as components of the causal prior[^2].

## BNNs as a target for approximation

The foundational PFN paper used BNN inference as a benchmark for approximating an intractable posterior: a BNN-prior PFN matched the performance of Bayes-by-Backprop SVI and NUTS while being 1,000×–10,000× faster[^3]. On 20+ small tabular datasets this BNN-prior PFN attained the best mean ROC AUC rank and best calibration, beating XGBoost and CatBoost[^4] — the direct precursor to TabPFN.

## Why SCMs took over

In the 2023 TabPFN, the prior mixed SCM and BNN generators with equal probability[^5], but an ablation found the SCM prior alone (0.881) outperformed the BNN prior (0.865), with mixing adding little[^6]. The 2025 model therefore centers on the causal generator, retaining neural-network computations only as edge mappings[^2]. The lesson: a prior that encodes causal structure fits real tables better than one built purely from random feedforward functions.

## Relationship to other concepts

BNNs are one generator of the [[synthetic-data-prior]] alongside [[structural-causal-models]], a historical target for [[posterior-predictive-distribution]] approximation, and — like SCMs — biased toward simplicity via [[occams-razor]].

## Notes

[^1]: [[muller-2022-pfn#^prior-bnn|Müller 2022, §prior-bnn]]
[^2]: [[hollmann-2025-tabpfn-nature#^edge-mappings|Hollmann 2025, §edge-mappings]]
[^3]: [[muller-2022-pfn#^exp-speedup|Müller 2022, §exp-speedup]]
[^4]: [[muller-2022-pfn#^exp-tabular|Müller 2022, §exp-tabular]]
[^5]: [[hollmann-2023-tabpfn#^prior-mix|Hollmann 2023, §prior-mix]]
[^6]: [[hollmann-2023-tabpfn#^scm-beats-bnn|Hollmann 2023, §scm-beats-bnn]]
