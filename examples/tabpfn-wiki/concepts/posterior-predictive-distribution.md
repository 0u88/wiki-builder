---
id: posterior-predictive-distribution
title: Posterior Predictive Distribution (PPD)
aliases: [PPD, posterior predictive distribution, posterior predictive]
tags: [bayesian, pfn]
status: draft
created: 2026-07-06
updated: 2026-07-06
sources: [muller-2022-pfn, hollmann-2023-tabpfn, hollmann-2025-tabpfn-nature]
---

**The posterior predictive distribution (PPD)** is the Bayesian prediction for a new point that averages over all hypotheses weighted by how well they fit the data and how likely they are a priori. For a latent task $t$ it is $p(y\mid x, D) = \int_t p(y\mid x, t)\, p(t\mid D)\, dt$[^1]. It is the quantity a [[prior-data-fitted-networks|PFN]] is trained to approximate: rather than computing the integral, the network learns to emit the PPD directly from the dataset given in context[^1]. The PPD is what ties [[tabpfn]]'s predictions to a well-defined [[synthetic-data-prior]].

## Definition

Writing $\Phi$ for the hypothesis space, the PPD integrates the likelihood over the posterior, or equivalently over the prior $p(\phi)$ reweighted by the data likelihood $p(D\mid\phi)$[^2]. Because the prior in TabPFN is an ensemble of data-generating mechanisms, the PPD "corresponds to an infinitely large ensemble" of such mechanisms — instantiations of [[structural-causal-models|SCMs]] and [[bayesian-neural-networks|BNNs]][^2]. This is Bayesian model averaging made concrete.

## Approximating it without a posterior

Traditional methods (NUTS/MCMC, variational inference) first approximate the posterior $p(t\mid D)$ and then integrate; PFNs "model the PPD directly … without ever instantiating the posterior"[^3]. The training loss is the cross-entropy between held-out targets and the model's prediction, $\mathbb{E}[-\log q(y_{\text{test}}\mid X_{\text{test}}, D_{\text{train}})]$[^4]. Minimizing this loss is equivalent to minimizing the KL divergence to the true PPD, and the minimizer recovers the exact PPD when it lies in the model family[^5]. This is the theoretical guarantee that a well-trained PFN is doing Bayesian inference.

## Evidence it holds in practice

For [[gaussian-process|Gaussian Processes]] with fixed hyperparameters — where the true PPD is tractable — a PFN's mean and 95% intervals are "virtually indistinguishable" from the exact PPD, improving as more meta-training datasets are used[^6]. When the true posterior is intractable (GP with hyper-priors), the PFN approximates the PPD *better* than MLE-II and NUTS while being orders of magnitude faster[^7].

## Relationship to other concepts

The PPD is the training target ([[prior-data-fitted-networks]]), realized through [[in-context-learning]], and defined relative to the [[synthetic-data-prior]]. Its regression form is emitted as a [[riemann-distribution]] over target values[^8].

## Notes

[^1]: [[muller-2022-pfn#^eq-ppd|Müller 2022, §eq-ppd]]
[^2]: [[hollmann-2023-tabpfn#^ppd-ensemble|Hollmann 2023, §ppd-ensemble]]
[^3]: [[muller-2022-pfn#^eq-ppd|Müller 2022, §eq-ppd]]
[^4]: [[hollmann-2025-tabpfn-nature#^ppd-loss|Hollmann 2025, §ppd-loss]]
[^5]: [[muller-2022-pfn#^thm-ppd|Müller 2022, §thm-ppd]]
[^6]: [[muller-2022-pfn#^exp-gp|Müller 2022, §exp-gp]]
[^7]: [[muller-2022-pfn#^exp-speedup|Müller 2022, §exp-speedup]]
[^8]: [[hollmann-2025-tabpfn-nature#^regression|Hollmann 2025, §regression]]
