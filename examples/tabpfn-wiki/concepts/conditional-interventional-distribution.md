---
id: conditional-interventional-distribution
title: Conditional Interventional Distribution (CID)
aliases: [CID, conditional interventional distribution, interventional distribution]
tags: [causal, treatment-effect]
status: draft
created: 2026-07-09
updated: 2026-07-09
sources: [robertson-2025-dopfn, balazadeh-2025-causalpfn]
---

**The conditional interventional distribution (CID)** is the estimand $p(y \mid \mathrm{do}(t), x)$ — the full distribution of the outcome $y$ under the intervention $\mathrm{do}(t)$ for units with covariates $x$[^1]. It is the central target of [[do-pfn]], which predicts it in a single forward pass from an observational dataset plus a query $(x, \mathrm{do}(t))$[^2]. Being a whole distribution (including aleatoric outcome noise), the CID is strictly richer than the expectation-level [[conditional-expected-potential-outcome]] that [[causalpfn]] targets.

## Definition

Using Pearl's $\mathrm{do}$-operator, the CID answers "what is the distribution of outcomes given features $x$ and intervention $\mathrm{do}(t)$"[^1]. Do-PFN outputs this distribution directly; the average treatment effect over covariates is then recovered as a difference of its expectations, $\tau(x) := \mathbb{E}[y \mid \mathrm{do}(1), x] - \mathbb{E}[y \mid \mathrm{do}(0), x]$[^3]. Predicting the full distribution rather than its mean lets Do-PFN represent [[ood-robustness|aleatoric spread]] and multimodality that a point estimate discards.

## Distribution vs expectation

The two 2025 causal PFNs make opposite choices here. Do-PFN targets the full interventional distribution, retaining aleatoric noise; CausalPFN targets its *expectation* $\mathbb{E}[Y_t \mid X]$ specifically to remove that noise and isolate epistemic uncertainty[^4]. The CID is therefore the do-operator object; CausalPFN uses the potential-outcomes framework and the do-operator only in passing[^4].

## How Do-PFN learns it

Do-PFN is trained on datasets sampled from [[structural-causal-models|SCMs]]: for each SCM it draws an observational dataset and then, holding the exogenous noise fixed, applies $\mathrm{do}(t)$ and reads off the interventional outcome[^5]. SGD on this data minimizes the expected forward KL to the true CID, giving a forward-KL-optimal approximation with respect to the SCM prior[^6]. Crucially, this does not require the causal graph or the [[strong-ignorability|unconfoundedness]] assumption; a prior over SCMs generalizes classical do-calculus, which fixes a single graph[^7].

## Relationship to other concepts

The CID is the distributional counterpart of the [[conditional-expected-potential-outcome]]; it is produced by [[amortized-causal-inference]] over [[structural-causal-models]], emitted as a [[histogram-loss-quantized-distribution|bar distribution]], and its uncertainty splits into aleatoric, [[observational-equivalence-unidentifiability|unidentifiability]], and epistemic parts.

## Notes

[^1]: [[robertson-2025-dopfn#^def-cid|Robertson 2025, §def-cid]]
[^2]: [[robertson-2025-dopfn#^def-dopfn|Robertson 2025, §def-dopfn]]
[^3]: [[robertson-2025-dopfn#^cate-from-cid|Robertson 2025, §cate-from-cid]]
[^4]: [[balazadeh-2025-causalpfn#^potential-outcomes|Balazadeh 2025, §potential-outcomes]]
[^5]: [[robertson-2025-dopfn#^train-intervention-sim|Robertson 2025, §train-intervention-sim]]
[^6]: [[robertson-2025-dopfn#^thm-forward-kl|Robertson 2025, §thm-forward-kl]]
[^7]: [[robertson-2025-dopfn#^no-unconfoundedness|Robertson 2025, §no-unconfoundedness]]
