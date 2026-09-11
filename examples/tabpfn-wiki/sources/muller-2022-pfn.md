---
id: muller-2022-pfn
title: "Transformers Can Do Bayesian Inference"
authors: [Müller, Hollmann, Arango, Grabocka, Hutter]
year: 2022
kind: paper
url: https://arxiv.org/abs/2112.10510
raw: raw/Mulleretal2022.pdf
ingested: 2026-07-06
---

Introduces **Prior-Data Fitted Networks (PFNs)**: a transformer is trained on datasets sampled from a prior to approximate the Bayesian posterior predictive distribution (PPD) for any prior one can sample from. Posterior approximation is recast as supervised learning — repeatedly sample a task and dataset from the prior, mask one label, and train the network to predict it in context. At inference a real dataset plus a query is fed in and the PFN outputs a predictive distribution approximating exact Bayesian inference in a single forward pass, giving 200×–10,000× speedups over MCMC/VI while matching Gaussian Processes and beating gradient-boosted trees on small tabular data.

## Key claims

- **def-pfn**: PFNs approximate a large set of posteriors by in-context learning; the only requirement is the ability to *sample* datasets from a prior over supervised tasks. Given samples from a new task, a PFN makes probabilistic predictions for arbitrary query points in a single forward pass, having learned to approximate Bayesian inference. (Abstract; §1; Fig. 1) ^def-pfn
- **def-icl**: At inference the trained PFN is fed the actual dataset together with a test point and outputs the prediction distribution conditioned on that dataset — "It performs in-context learning … this distribution approximates exact Bayesian posterior prediction." (§1, p.2) ^def-icl
- **eq-ppd**: The posterior predictive distribution is $p(y\mid x, D) = \int_t p(y\mid x, t)\, p(t\mid D)\, dt$ (Eq. 1, §2). Traditional methods (NUTS/MCMC, variational inference) first approximate the posterior $p(t\mid D)$; PFNs model the PPD directly without ever instantiating the posterior. (§2, p.3) ^eq-ppd
- **eq-loss**: The training objective is the Prior-Data Negative Log-Likelihood $\ell_\theta = \mathbb{E}_{D \cup \{(x,y)\} \sim p(D)}\!\left[ -\log q_\theta(y \mid x, D) \right]$ (Eq. 2, §3), optimized by Algorithm 1: sample datasets from the prior and predict a held-out example. (§3, p.4) ^eq-loss
- **thm-ppd**: Minimizing $\ell_\theta$ is equivalent to minimizing the expected cross-entropy / KL divergence between the true PPD and the model $q_\theta$ (Insight 1, Corollary 1.1); if the true PPD lies in the model family, the optimum satisfies $q_{\theta^*}(\cdot\mid x, D) = p(\cdot\mid x, D)$ — i.e. minimizing the loss recovers the exact PPD (Corollary 1.2; proofs App. A–B). (§3, p.4) ^thm-ppd
- **arch-transformer**: The model is a Transformer encoder *without positional encodings*, making it permutation-invariant over dataset examples; $(x,y)$ pairs enter as summed linear encodings, and an attention mask lets every input attend to every other input while queries attend to inputs only. (§4; App. E.1; Fig. 2a) ^arch-transformer
- **arch-riemann**: A novel regression head, the **Riemann distribution**, discretizes continuous output into equal-probability buckets (bar-plot PDF); Theorem 1 shows it can approximate any Riemann-integrable, a.e.-continuous density to arbitrary precision. (§4; Fig. 2b–c; App. C, E.2) ^arch-riemann
- **exp-gp**: For Gaussian Processes with fixed hyperparameters (tractable ground-truth PPD), the PFN's mean and 95% intervals are virtually indistinguishable from the exact PPD, improving as more meta-train datasets are used. (§5.1; Figs. 3, 4a) ^exp-gp
- **exp-speedup**: On a GP with hyper-priors the PFN approximates the PPD better than MLE-II and NUTS while being >200× faster than MLE-II and 1,000×–8,000× faster than NUTS; a BNN-prior PFN is 1,000× faster than Bayes-by-Backprop SVI and 10,000× faster than NUTS at matched performance. (§5.2–5.3; Figs. 4b, 5) ^exp-speedup
- **prior-bnn**: A Bayesian Neural Network prior generates data by sampling random weights (and, optionally, a random architecture) and i.i.d. normal features, then propagating them forward; the PFN is thereby Bayesian over both weights and architecture in one inference. (§5.3, §6; App. G; Fig. 6) ^prior-bnn
- **exp-tabular**: On 20+ small OpenML tabular datasets (30 training samples), a BNN-prior PFN attains the best mean ROC AUC rank (2.786 vs XGBoost 3.357, CatBoost 4.833) and best calibration (ECE 0.025), classifying all datasets in ~13 s on a V100 — >5000× faster than the ~20 h XGBoost tuning. (§6; Tables 1, 7) ^exp-tabular
- **handling-features**: Datasets with varying feature counts are handled by fixing a max feature count (60), zero-padding, and rescaling features by $\text{max\_features}/\text{features\_used}$ to keep input scale constant; each subset is standardized using only model-visible samples. (App. G) ^handling-features
- **tuning-free**: The optimization "does not allow for overfitting" — lower training loss always means closeness to the exact posterior, so more training only improves performance and calibration; a single trained model is reused across datasets with no per-dataset tuning (only a one-time prior-hyperparameter grid search). (§1, §6; App. D, G) ^tuning-free

## Notes

- Concepts introduced only in the later TabPFN papers and **absent here**: Structural Causal Model priors, KV/state caching for inference, and the explicit "foundation model" and "Occam's razor" framings. This paper's generality is shown empirically across GP, BNN, tabular, and few-shot image priors rather than named as a foundation-model property.
