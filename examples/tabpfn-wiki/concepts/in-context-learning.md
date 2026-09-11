---
id: in-context-learning
title: In-Context Learning (ICL)
aliases: [ICL, in context learning, in-context learning]
tags: [in-context-learning, pfn, transformer]
status: draft
created: 2026-07-06
updated: 2026-07-06
sources: [muller-2022-pfn, hollmann-2023-tabpfn, hollmann-2025-tabpfn-nature]
---

**In-context learning (ICL)** is the mechanism by which a [[prior-data-fitted-networks|PFN]] "learns" from a dataset supplied as input rather than through gradient updates: the labeled training set and the query points are fed together as one set-valued input, and predictions come out of a single forward pass[^1]. It is the same capability that lets large language models adapt from examples in their prompt[^2], repurposed here so that the entire training set of a tabular problem becomes the context. Because no gradient descent happens at inference time, ICL is what makes [[tabpfn]] fast and tuning-free.

## The mechanism

At inference the trained model is given the actual dataset together with a test point and outputs the prediction distribution conditioned on that dataset — "It performs in-context learning … this distribution approximates exact Bayesian posterior prediction"[^3]. TabPFN "learn[s] from sequences of labeled examples … without requiring further parameter updates" and "does not use gradient-based learning on data seen at inference time," behaving like a [[gaussian-process|Gaussian Process]] in that respect[^1]. The 2025 model makes the framing explicit: training and prediction "happen in a single … forward pass," with training samples given as context[^2].

## Why it works for tabular data

The training set is treated as an unordered set, not a sequence, which is enforced architecturally (see [[2d-transformer-architecture]] and [[permutation-invariance]]): test tokens attend to training tokens but training tokens are exchangeable[^4]. This lets one pre-trained network be applied to any new table without retraining, and is the operational form of approximating the [[posterior-predictive-distribution]] — the context *is* the conditioning dataset $D$ in $p(y\mid x, D)$.

## Consequences

ICL is why TabPFN needs [[zero-hyperparameter-tuning]]: there are no training hyperparameters to set at inference because there is no training at inference[^5]. It also creates a cost profile unlike gradient-trained models — the whole training set must be processed on every prediction — which motivates [[state-caching-inference]] to avoid recomputing the training-set representation[^6].

## Notes

[^1]: [[hollmann-2023-tabpfn#^icl|Hollmann 2023, §icl]]
[^2]: [[hollmann-2025-tabpfn-nature#^icl|Hollmann 2025, §icl]]
[^3]: [[muller-2022-pfn#^def-icl|Müller 2022, §def-icl]]
[^4]: [[hollmann-2025-tabpfn-nature#^2d-arch|Hollmann 2025, §2d-arch]]
[^5]: [[hollmann-2025-tabpfn-nature#^no-tuning|Hollmann 2025, §no-tuning]]
[^6]: [[hollmann-2025-tabpfn-nature#^state-caching|Hollmann 2025, §state-caching]]
