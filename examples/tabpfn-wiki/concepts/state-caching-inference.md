---
id: state-caching-inference
title: State Caching and Efficient Inference
aliases: [state caching, KV caching, efficient inference, key-value caching, training-set caching]
tags: [inference, tabpfn, transformer]
status: draft
created: 2026-07-06
updated: 2026-07-06
sources: [hollmann-2023-tabpfn, hollmann-2025-tabpfn-nature]
---

**State caching** is the optimization that makes repeated TabPFN predictions cheap: because the representation of the training samples does not depend on the test set, TabPFN caches the training samples' attention keys and values and reuses them across all queries instead of recomputing the [[in-context-learning|in-context]] pass every time[^1]. Introduced in the 2025 Nature model, it turns the "process the whole training set on every prediction" cost of a [[prior-data-fitted-networks|PFN]] into a one-time computation, and is a large part of why [[tabpfn]] can serve predictions in a fraction of a second.

## The idea

In the [[2d-transformer-architecture]], test samples attend only to training data, never to each other[^2]. That independence means the keys/values derived from the training cells are fixed once the training set is given. TabPFN exploits this with a multi-query-attention variant that stores roughly one key/value pair per training cell, so [[in-context-learning]] on the training set is done once and reused for every test point[^1]. The measured effect is large: on 10,000 samples with 10 features, caching gives roughly 300× CPU (32 s → 0.1 s) and 6× GPU speedups, rising to 800× CPU and 30× GPU at 100 features[^1].

## Efficiency in the 2023 model (before caching)

The original TabPFN did not describe a caching mechanism; its "under a second" speed came from doing prediction in a single forward pass and from shrinking the attention matrix from $(n+m)^2$ to $n^2 + n\cdot m$ for $n$ training and $m$ test points[^3]. That already yielded a 230× CPU / 5,700× GPU speedup over AutoML systems tuning for an hour[^3]. State caching is the 2025 generation's further step, targeting the repeated-query and larger-dataset regime.

## Cost profile and its limits

Compute scales quadratically in samples and features, $O(n^2 + m^2)$, and memory only linearly, $O(nm)$, with engineering optimizations cutting memory below 1,000 bytes/cell to fit up to 50 million cells on one H100[^4]. Caching does not remove TabPFN's stated inference-cost limitation: for a single-sample prediction a highly optimized CatBoost can still be far faster (0.0002 s vs 0.2 s on 10k×10 data), and memory grows with dataset size[^5]. Caching helps most exactly when the same fitted training set is queried many times.

## Relationship to other concepts

State caching is enabled by the cell-wise [[2d-transformer-architecture]] and the query-independence of [[in-context-learning]]; together with [[zero-hyperparameter-tuning]] it underpins the speed claims of the [[tabular-foundation-model]].

## Notes

[^1]: [[hollmann-2025-tabpfn-nature#^state-caching|Hollmann 2025, §state-caching]]
[^2]: [[hollmann-2025-tabpfn-nature#^2d-arch|Hollmann 2025, §2d-arch]]
[^3]: [[hollmann-2023-tabpfn#^speed|Hollmann 2023, §speed]]
[^4]: [[hollmann-2025-tabpfn-nature#^complexity|Hollmann 2025, §complexity]]
[^5]: [[hollmann-2025-tabpfn-nature#^limitations|Hollmann 2025, §limitations]]
