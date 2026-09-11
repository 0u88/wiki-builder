---
id: 2d-transformer-architecture
title: 2D Transformer Architecture for Tables
aliases: [2D transformer, two-way attention, table transformer, cell-wise attention, two-dimensional attention]
tags: [transformer, tabpfn, tabular]
status: draft
created: 2026-07-06
updated: 2026-07-06
sources: [muller-2022-pfn, hollmann-2023-tabpfn, hollmann-2025-tabpfn-nature]
---

**The 2D transformer architecture** is TabPFN v2's table-native design in which every *cell* of the table gets its own representation and attention runs in two directions — across features within a row, and across samples within a column[^1]. This replaces the 2023 model's one-token-per-row scheme[^2] and is what makes [[tabpfn]] invariant to both the order of samples and the order of features, and able to extrapolate to more rows and columns than it saw in training[^1]. It is the concrete realization of [[in-context-learning]] over tabular data.

## From row-tokens to cell-tokens

The 2023 TabPFN encoded each feature-vector-plus-label as a single token and split self-attention into two weight-sharing modules: self-attention among training examples and cross-attention from test examples to training examples[^2]. The 2025 model instead assigns a separate representation to each cell and applies a two-way attention: first 1D attention over the features within a sample, then 1D attention over the samples within a feature, followed by an MLP sublayer, each wrapped in residual connections and half-precision layer norm[^1]. The default stacks 12 such 2D layers[^1].

## Permutation invariance and extrapolation

Both generations feed the training set as an unordered set rather than a sequence — there are no positional encodings, so the model is permutation-invariant over examples[^3] (see [[permutation-invariance]]). The 2D scheme extends this to features, so column order does not matter either, and lets the model generalize to table shapes beyond training[^1]. In all versions, test samples attend only to training data, never to each other[^1] — the structural expression of conditioning on the training set $D$.

## Cost and memory

Compute scales quadratically in both samples and features, $O(n^2 + m^2)$, while memory scales linearly, $O(nm)$[^4]. Engineering optimizations — half-precision layer norms, flash attention, activation checkpointing, and sequential state computation — cut memory roughly 4× to under 1,000 bytes per cell, enabling up to 50 million cells on a single H100 GPU[^4]. This cell-wise layout is also what makes [[state-caching-inference]] possible, since each training cell has a cacheable key/value.

## Relationship to other concepts

The 2D transformer is the substrate for [[in-context-learning]] and [[state-caching-inference]], relies on [[permutation-invariance]], and its cell-level inputs are what let TabPFN absorb the messiness handled in [[handling-tabular-peculiarities]]. The regression head atop it emits a [[riemann-distribution]].

## Notes

[^1]: [[hollmann-2025-tabpfn-nature#^2d-arch|Hollmann 2025, §2d-arch]]
[^2]: [[hollmann-2023-tabpfn#^two-module-attention|Hollmann 2023, §two-module-attention]]
[^3]: [[muller-2022-pfn#^arch-transformer|Müller 2022, §arch-transformer]]
[^4]: [[hollmann-2025-tabpfn-nature#^complexity|Hollmann 2025, §complexity]]
