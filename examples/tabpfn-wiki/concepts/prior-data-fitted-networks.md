---
id: prior-data-fitted-networks
title: Prior-Data Fitted Networks (PFNs)
aliases: [PFN, PFNs, prior-data fitted network, prior-data fitted networks, prior data fitted network]
tags: [pfn, bayesian, in-context-learning]
status: draft
created: 2026-07-06
updated: 2026-07-06
sources: [muller-2022-pfn, hollmann-2023-tabpfn, hollmann-2025-tabpfn-nature]
---

**Prior-Data Fitted Networks (PFNs)** are transformers trained to approximate Bayesian prediction by learning from datasets drawn from a prior, so that a single forward pass over a labeled dataset and a query point yields an approximation of the Bayesian posterior predictive distribution[^1]. The only requirement is the ability to *sample* datasets from a prior over supervised tasks — posterior approximation is thereby recast as ordinary supervised learning[^1]. PFNs are the framework underlying [[tabpfn]]; they realize Bayesian [[in-context-learning]] and target the [[posterior-predictive-distribution]] directly without ever instantiating a posterior.

## Definition and motivation

Classical Bayesian prediction requires approximating the posterior $p(t\mid D)$ over some latent task $t$ (via MCMC or variational inference) and then integrating to get predictions. PFNs skip the posterior entirely: they "model the PPD directly … without ever instantiating the posterior"[^2]. Given samples from a new task, a trained PFN "make[s] probabilistic predictions for arbitrary other data points in a single forward propagation, having learned to approximate Bayesian inference"[^1]. This is what makes prediction fast — there is no per-dataset optimization at inference time.

## How a PFN is trained

Training is offline and done once. Datasets are repeatedly sampled from a [[synthetic-data-prior]], one label is held out, and the network is trained to predict it from the rest of the dataset given as context[^3]. The objective is the **Prior-Data Negative Log-Likelihood**,

$$
\ell_\theta = \mathbb{E}_{D \cup \{(x,y)\} \sim p(D)}\!\left[ -\log q_\theta(y \mid x, D) \right],
$$

a plain cross-entropy over held-out targets[^3]. Minimizing it is equivalent to minimizing the KL divergence between the true PPD and the model, and if the true PPD lies in the model family the optimum recovers it exactly[^4]. Because lower training loss always means closeness to the exact posterior, the training problem "does not allow for overfitting" in the usual sense[^5].

## From PFNs to TabPFN

[[tabpfn]] is the PFN whose prior is designed for tabular data[^6]. The original 2023 model was a 12-layer, ${\sim}26$M-parameter transformer trained on ${\sim}9.2$M synthetic datasets[^7]; the 2025 Nature version scales training to ${\sim}100$M synthetic datasets and adds regression and much larger inputs[^8]. The generality of the framework was first shown by mimicking [[gaussian-process|Gaussian Processes]] and [[bayesian-neural-networks|Bayesian Neural Networks]] as priors[^9], anticipating the [[tabular-foundation-model]] framing.

## Relationship to other concepts

PFNs sit at the intersection of [[in-context-learning]] (the inference mechanism), the [[posterior-predictive-distribution]] (the training target), and the [[synthetic-data-prior]] (the source of training data). Their inductive bias comes entirely from the prior, which is where [[occams-razor|simplicity]] and [[structural-causal-models|causal structure]] enter.

## Notes

[^1]: [[muller-2022-pfn#^def-pfn|Müller 2022, §def-pfn]]
[^2]: [[muller-2022-pfn#^eq-ppd|Müller 2022, §eq-ppd]]
[^3]: [[muller-2022-pfn#^eq-loss|Müller 2022, §eq-loss]]
[^4]: [[muller-2022-pfn#^thm-ppd|Müller 2022, §thm-ppd]]
[^5]: [[muller-2022-pfn#^tuning-free|Müller 2022, §tuning-free]]
[^6]: [[hollmann-2023-tabpfn#^pfn-def|Hollmann 2023, §pfn-def]]
[^7]: [[hollmann-2023-tabpfn#^training-scale|Hollmann 2023, §training-scale]]
[^8]: [[hollmann-2025-tabpfn-nature#^training-scale|Hollmann 2025, §training-scale]]
[^9]: [[muller-2022-pfn#^exp-gp|Müller 2022, §exp-gp]]
