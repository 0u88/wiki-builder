---
id: synthetic-data-prior
title: Synthetic Data Prior
aliases: [synthetic prior, synthetic data prior, dataset prior, prior over datasets]
tags: [prior, pfn, bayesian]
status: draft
created: 2026-07-06
updated: 2026-07-06
sources: [muller-2022-pfn, hollmann-2023-tabpfn, hollmann-2025-tabpfn-nature]
---

**The synthetic data prior** is the distribution over entire datasets that a [[prior-data-fitted-networks|PFN]] is trained on: instead of collecting real data, one *samples* fictitious datasets from a generative process and trains the network to predict held-out labels within them[^1]. Because a PFN approximates the [[posterior-predictive-distribution]] for whatever prior generated its training data, this prior is the model's entire inductive bias — choosing it is the central design act in building [[tabpfn]]. TabPFN's prior is built from [[structural-causal-models]] and [[bayesian-neural-networks]] with a bias toward [[occams-razor|simple]] structures.

## Why datasets, not data points

The only requirement to train a PFN is that one can sample datasets from the prior[^1]. This turns Bayesian posterior approximation into supervised learning: each training example is a whole dataset with one target masked out, and averaging over millions of such datasets teaches the network to integrate over the hypothesis space[^2]. The prior thus plays the role that a kernel plays for a [[gaussian-process|Gaussian Process]] — it encodes assumptions about which functions and datasets are plausible.

## What TabPFN samples

In the 2023 model, each synthetic dataset is drawn "from either one or the other prior with equal probability" — an [[structural-causal-models|SCM]] prior or a [[bayesian-neural-networks|BNN]] prior — generating a regression task that is then converted to classification[^3]. An ablation found the SCM prior alone (ROC AUC 0.881) outperformed the BNN prior (0.865), with mixing barely changing results, identifying the SCM prior as the key contribution[^4]. The 2025 Nature model centers the prior on SCMs whose edges apply small neural networks, categorical discretization, decision trees, and injected Gaussian noise[^5].

## Scale of the sampling

The prior is consumed at enormous scale during offline training: ${\sim}9.2$M synthetic datasets for the 2023 model[^6] and ${\sim}100$M for the 2025 model, each drawn with feature counts, sizes, and difficulty sampled from high-level hyperparameters[^7]. A single Bayesian ensemble integrates over these hyperparameters, so no per-dataset choices remain — the foundation of [[zero-hyperparameter-tuning]][^8].

## Relationship to other concepts

The synthetic prior defines the [[posterior-predictive-distribution]] the PFN targets; its generators are [[structural-causal-models]] and [[bayesian-neural-networks]]; its bias toward simplicity is [[occams-razor]]. Notably, the code generating the 2025 prior was not publicly released[^9].

## Notes

[^1]: [[muller-2022-pfn#^def-pfn|Müller 2022, §def-pfn]]
[^2]: [[muller-2022-pfn#^eq-loss|Müller 2022, §eq-loss]]
[^3]: [[hollmann-2023-tabpfn#^prior-mix|Hollmann 2023, §prior-mix]]
[^4]: [[hollmann-2023-tabpfn#^scm-beats-bnn|Hollmann 2023, §scm-beats-bnn]]
[^5]: [[hollmann-2025-tabpfn-nature#^edge-mappings|Hollmann 2025, §edge-mappings]]
[^6]: [[hollmann-2023-tabpfn#^training-scale|Hollmann 2023, §training-scale]]
[^7]: [[hollmann-2025-tabpfn-nature#^scm-prior|Hollmann 2025, §scm-prior]]
[^8]: [[hollmann-2025-tabpfn-nature#^training-scale|Hollmann 2025, §training-scale]]
[^9]: [[hollmann-2025-tabpfn-nature#^limitations|Hollmann 2025, §limitations]]
