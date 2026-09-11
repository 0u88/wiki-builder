---
id: occams-razor
title: Occam's Razor and Simplicity
aliases: [Occam's razor, occams razor, simplicity prior, simplicity bias, speed prior]
tags: [prior, bayesian, tabpfn]
status: draft
created: 2026-07-06
updated: 2026-07-06
sources: [hollmann-2023-tabpfn, hollmann-2025-tabpfn-nature]
---

**Occam's razor** in TabPFN is the deliberate bias of its [[synthetic-data-prior]] toward simple data-generating structures: among the [[structural-causal-models|SCMs]] and [[bayesian-neural-networks|BNNs]] used to generate synthetic datasets, "simpler … (with fewer parameters) have a higher likelihood"[^1]. Because a [[prior-data-fitted-networks|PFN]] inherits its entire inductive bias from its prior, this simplicity preference is *how* [[tabpfn]] favors parsimonious explanations of a dataset — the Bayesian analogue of preferring the simplest model that fits. It distinguishes TabPFN's inductive bias from that of gradient-boosted trees.

## How simplicity is encoded

The 2023 prior draws on Occam's razor and Schmidhuber's Speed Prior: simpler causal graphs and networks are made more likely, implemented for example as a log-scaled uniform distribution over the average number of SCM nodes, so small, few-parameter graphs dominate[^1]. In the 2025 model the same idea appears as controlled graph-size and edge-density hyperparameters — the number of nodes is drawn log-uniform and a Bayesian ensemble integrates over these complexity knobs, biasing toward diverse but controllable (including sparse) structures[^2].

## Evidence the bias is real

An ablation in the 2023 paper confirms TabPFN's predictions are biased toward simple causal explanations in a way gradient-boosted trees are not[^1]. This is not merely aesthetic: because the [[posterior-predictive-distribution]] averages over the prior, weighting simple mechanisms more heavily changes what the model predicts on ambiguous data, typically improving generalization on the small datasets TabPFN targets.

## Why it matters for small data

On small datasets many hypotheses fit the training points equally well, and the prior is what breaks the tie. A simplicity-weighted prior means TabPFN resolves that ambiguity toward parsimonious causal structure, which is a large part of why it performs well with few samples and needs [[zero-hyperparameter-tuning]] to avoid overfitting.

## Relationship to other concepts

Occam's razor is a property of the [[synthetic-data-prior]], expressed through the complexity controls of [[structural-causal-models]] and [[bayesian-neural-networks]], and it shapes the [[posterior-predictive-distribution]] the [[prior-data-fitted-networks|PFN]] learns. Note the 2025 paper frames this as covering diverse scenarios rather than using the explicit phrase "Occam's razor"[^2].

## Notes

[^1]: [[hollmann-2023-tabpfn#^occam|Hollmann 2023, §occam]]
[^2]: [[hollmann-2025-tabpfn-nature#^graph-sampling|Hollmann 2025, §graph-sampling]]
