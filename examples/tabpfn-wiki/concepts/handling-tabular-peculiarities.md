---
id: handling-tabular-peculiarities
title: Handling Tabular Peculiarities
aliases: [tabular peculiarities, handling tabular data, tabular data handling, tabular preprocessing]
tags: [tabular, tabpfn]
status: draft
created: 2026-07-06
updated: 2026-07-08
sources: [muller-2022-pfn, hollmann-2023-tabpfn, hollmann-2025-tabpfn-nature]
---

**Handling tabular peculiarities** refers to the machinery that lets TabPFN accept raw, messy tables — varying feature counts, missing values, categorical columns, wildly different scales, uninformative columns, and outliers — with minimal preprocessing[^1]. These are the properties that make tabular data harder for generic deep nets than images or text, and addressing them is much of what separates a working [[tabular-foundation-model]] from the raw [[prior-data-fitted-networks|PFN]] idea. TabPFN's strategy is twofold: light input transforms, plus a [[synthetic-data-prior]] that deliberately generates the same messiness so the model learns to cope during pre-training.

## Varying feature counts

Because one pre-trained network must serve tables of any width, the feature dimension is treated flexibly. In 2023 the feature count is drawn uniformly up to 100 during training, and datasets are zero-padded to the maximum $K$ with padded features scaled by $K/k$ to preserve magnitude[^2]; the foundational PFN used the same trick with a cap of 60 features and rescaling by $\text{max\_features}/\text{features\_used}$[^3]. The [[2d-transformer-architecture]] later removed the need to pad to a fixed width by treating features as a second attention axis.

## Missing values, categoricals, and scale

The 2023 model normalizes inputs to zero mean/unit variance with Yeo–Johnson power scaling for exponential data, replaces missing values with zero (no special NaN handling), and assigns categorical features to a random fraction of columns (20% probability) during prior-fitting[^4]. The 2025 model handles missing values more explicitly with a per-cell "missing" indicator (value set to 0, and synthetic data masked MCAR), integer-encodes categoricals, and z-normalizes features so that scaling does not affect predictions[^1].

## Robustness to uninformative features and outliers

A distinctive claim of the 2025 model is robustness: with only half the samples TabPFN still matches the next-best method using all samples, and it tolerates uninformative columns and outliers[^1]. This is not accidental — the [[structural-causal-models|SCM]] prior deliberately produces uninformative predictors via disjoint subgraphs and injects noise, so the model meets such columns constantly during training[^5]. The principle is *generate the peculiarity in the prior, learn to ignore it*.

This robustness was a direct answer to a stated weakness of the 2023 model, whose prior "did not consider the existence of many uninformative features," leading to performance degradation when such features were added, and whose performance was "generally worse" on datasets with categorical features and/or missing values[^6]. Making the prior *generate* these peculiarities is precisely what closed that gap in v2.

## Relationship to other concepts

Robust handling is enabled by the [[2d-transformer-architecture]] and taught through the [[synthetic-data-prior]] and its [[structural-causal-models]]; together with regression support it is central to TabPFN's [[tabular-foundation-model]] claim, and it removes preprocessing choices that would otherwise be [[zero-hyperparameter-tuning|hyperparameters]].

## Notes

[^1]: [[hollmann-2025-tabpfn-nature#^peculiarities|Hollmann 2025, §peculiarities]]
[^2]: [[hollmann-2023-tabpfn#^flexible-features|Hollmann 2023, §flexible-features]]
[^3]: [[muller-2022-pfn#^handling-features|Müller 2022, §handling-features]]
[^4]: [[hollmann-2023-tabpfn#^preprocessing|Hollmann 2023, §preprocessing]]
[^5]: [[hollmann-2025-tabpfn-nature#^graph-sampling|Hollmann 2025, §graph-sampling]]
[^6]: [[hollmann-2023-tabpfn#^limitations-2023|Hollmann 2023, §limitations-2023]]
