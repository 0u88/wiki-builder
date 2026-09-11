---
id: structural-causal-models
title: Structural Causal Models (SCMs)
aliases: [SCM, SCMs, structural causal model, structural causal models, causal prior]
tags: [prior, tabpfn]
status: draft
created: 2026-07-06
updated: 2026-07-06
sources: [hollmann-2023-tabpfn, hollmann-2025-tabpfn-nature]
---

**A structural causal model (SCM)** is a directed acyclic graph of variables in which each node is a deterministic-plus-noise function of its parents, $z_i = f_i(z_{\text{PA}(i)}, \epsilon_i)$[^1]. In TabPFN, SCMs are the generative backbone of the [[synthetic-data-prior]]: each synthetic dataset is produced by sampling a causal graph, pushing noise through it, and reading off features and a target at randomly chosen nodes[^1]. Training on datasets generated this way is what biases [[tabpfn]] toward the kind of causally-structured dependencies that real tabular data tends to exhibit — and it is the single change that most improved performance over a plain [[bayesian-neural-networks|BNN]] prior[^2].

## How an SCM generates a dataset

In the 2023 model, an SCM is instantiated from an $l$-layer MLP: edge weights are sampled, a random subset of edges is dropped to yield a DAG, then feature nodes and one label node are sampled from the graph, with each node computing $z_i = a\big((\sum_j E_{ij} z_j) + \epsilon_i\big)$ for a per-dataset activation from {Tanh, LeakyReLU, ELU, Identity}[^3]. The 2025 model generalizes this: high-level hyperparameters are sampled, a causal DAG is constructed, "initialization data" (noise) is propagated through the root nodes, and feature/target values are read off at sampled node positions[^1].

## Edge computations and graph shape

In the Nature model, edges apply four module types — small neural networks (linear maps with nonlinear activations such as log, sine, tanh, ReLU, rank, squaring, step, modulo), categorical discretization, decision trees for rule-based dependencies, and Gaussian noise injection $\mathcal{N}(0,\sigma^2 I)$ at each edge[^4]. Graphs are sampled with a "growing network with redirection" preferential-attachment scheme that yields scale-free structures, with graph size and edge density as controlled hyperparameters a Bayesian ensemble integrates over[^5]. Disjoint subgraphs deliberately create features that are marginally independent of the target — synthetic *uninformative predictors* (see [[handling-tabular-peculiarities]])[^5].

## Why causal structure helps

Because the target is read off a node embedded in a causal graph, dependencies among features and between features and target mirror the shared-cause and mediated relationships found in real data. An ablation showed the SCM prior (ROC AUC 0.881) beats the BNN prior (0.865), and combining them barely changes results — the novel SCM prior is the key contribution of the 2023 paper[^2]. The bias toward smaller, sparser graphs is where [[occams-razor]] enters the prior.

## Relationship to other concepts

SCMs are one of the two generators of the [[synthetic-data-prior]] (the other being [[bayesian-neural-networks]]); their graph-size control implements [[occams-razor]]; and the datasets they produce are what train the [[prior-data-fitted-networks|PFN]] to approximate the [[posterior-predictive-distribution]].

## Notes

[^1]: [[hollmann-2025-tabpfn-nature#^scm-prior|Hollmann 2025, §scm-prior]]
[^2]: [[hollmann-2023-tabpfn#^scm-beats-bnn|Hollmann 2023, §scm-beats-bnn]]
[^3]: [[hollmann-2023-tabpfn#^scm-from-mlp|Hollmann 2023, §scm-from-mlp]]
[^4]: [[hollmann-2025-tabpfn-nature#^edge-mappings|Hollmann 2025, §edge-mappings]]
[^5]: [[hollmann-2025-tabpfn-nature#^graph-sampling|Hollmann 2025, §graph-sampling]]
