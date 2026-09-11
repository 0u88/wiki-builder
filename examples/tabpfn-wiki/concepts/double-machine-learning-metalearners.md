---
id: double-machine-learning-metalearners
title: Double Machine Learning and Meta-Learners
aliases: [DML, double machine learning, meta-learners, T-learner, S-learner, X-learner, TSX-learners]
tags: [causal, treatment-effect]
status: draft
created: 2026-07-09
updated: 2026-07-09
sources: [balazadeh-2025-causalpfn, robertson-2025-dopfn]
---

**Double machine learning (DML) and meta-learners** are the standard families of machine-learning-based treatment-effect estimators against which the causal PFNs are benchmarked. Meta-learners (the S-, T-, and X-Learners) reduce [[conditional-expected-potential-outcome|CATE]] estimation to fitting ordinary regressors on the treated and control groups; DML uses cross-fitted nuisance models with a Neyman-orthogonal score to debias the effect estimate. In both [[causalpfn]] and [[do-pfn]] these are the *baselines* — per-dataset estimators, usually with their own hyperparameter tuning, that the amortized [[amortized-causal-inference|forward-pass]] models aim to match or beat[^1].

## The baseline families

Across the two papers the compared estimators include the S/T/X-Learners and a DA-Learner, DR-Learner, Forest DML (Wager–Athey causal forests / generalized random forests), and deep CATE models such as TARNet, DragonNet, and RA-Net[^1][^2]. The meta-learner naming is by construction: an **S-Learner** fits one model with treatment as a feature, a **T-Learner** fits separate models per treatment arm, and an **X-Learner** adds a cross-imputation step for better performance under group imbalance. DML instead estimates outcome and propensity nuisances separately and combines them through an orthogonal moment so that small nuisance errors do not bias the effect.

## How the PFNs compare

The amortized models are competitive to superior while avoiding per-dataset fitting. CausalPFN attains the best average CATE rank ($2.30 \pm 0.10$ by PEHE) across 310 realizations of IHDP, ACIC 2016, and Lalonde, with most baselines tuned via cross-validated grid search[^1]. Do-PFN significantly outperforms the S/T/X-Learners, a causal-forest DML approach, and the deep methods DragonNet and TARNet in CATE and ATE estimation on its synthetic case studies[^2]. A notable data point: plain [[tabpfn]], using its regression output as a CEPO proxy, is already "surprisingly competitive" as a causal baseline, and fine-tuning it on CausalPFN's causal prior improves it further — evidence that the identifiable prior, not just the architecture, carries the gain[^3].

## Relationship to other concepts

DML and meta-learners are the non-amortized alternative to [[amortized-causal-inference]]; they target the same [[conditional-expected-potential-outcome|CEPO/CATE]] estimands and rely on the same [[strong-ignorability]] assumption, and they are evaluated with the same [[integrated-coverage-error|coverage]] and PEHE metrics.

## Notes

[^1]: [[balazadeh-2025-causalpfn#^results-table1|Balazadeh 2025, §results-table1]]
[^2]: [[robertson-2025-dopfn#^results|Robertson 2025, §results]]
[^3]: [[balazadeh-2025-causalpfn#^vs-tabpfn|Balazadeh 2025, §vs-tabpfn]]
