---
id: hollmann-2023-tabpfn
title: "TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second"
authors: [Hollmann, Müller, Eggensperger, Hutter]
year: 2023
kind: paper
url: https://arxiv.org/abs/2207.01848
raw: raw/Hollmannetal2023.pdf
ingested: 2026-07-06
---

Introduces **TabPFN**, a single pre-trained transformer that classifies small tabular datasets in under a second with no per-dataset training or hyperparameter tuning. It is a Prior-Data Fitted Network: trained once offline to approximate the Bayesian posterior predictive distribution over synthetic datasets drawn from a hand-designed prior that mixes Structural Causal Models and Bayesian Neural Networks with a built-in preference for simple structures. At inference the labeled training set and test points are fed as one set-valued input and predictions come out of a single forward pass. On 18 small numerical OpenML-CC18 datasets it matches AutoML systems that tune for an hour, with a 230× (CPU) to 5,700× (GPU) speedup.

## Key claims

- **pfn-def**: TabPFN is a Prior-Data Fitted Network trained offline once to approximate Bayesian inference / the PPD on synthetic datasets from a prior; minimizing cross-entropy on held-out synthetic examples (Eq. 2) approximates the true Bayesian PPD. (Abstract; §2, p.2; §3, p.3) ^pfn-def
- **icl**: TabPFN performs in-context learning — it learns from labeled examples given in the input "without requiring further parameter updates," predicting the whole test set in a single forward pass and using no gradient-based learning on inference-time data (like a Gaussian Process). (Abstract; §2 "Real-World Inference," p.3) ^icl
- **ppd-ensemble**: The PPD integrates over the hypothesis space $\Phi$ weighted by prior $p(\phi)$ and likelihood $p(D\mid\phi)$ (Eq. 1) and thus "corresponds to an infinitely large ensemble" of data-generating mechanisms (SCM and BNN instantiations). (§1–2, p.2) ^ppd-ensemble
- **prior-mix**: The prior mixes an SCM prior and a BNN prior, drawn "from either one or the other prior with equal probability" during prior-fitting; both generate regression tasks later converted to classification. (§4.3–4.4, p.5) ^prior-mix
- **scm-from-mlp**: SCMs are instantiated from an $l$-layer MLP with hidden size $h$: sample edge weights, drop a random set of edges to yield a random DAG, sample feature nodes and one label node, with each node $z_i = a\big((\sum_j E_{ij} z_j) + \epsilon_i\big)$ and one activation per dataset from {Tanh, LeakyReLU, ELU, Identity}. (App. C.1, p.26; Fig. 2) ^scm-from-mlp
- **occam**: The prior is based on simplicity (Occam's Razor / Schmidhuber's Speed Prior) — "simpler SCMs and BNNs (with fewer parameters) have a higher likelihood," e.g. a log-scaled uniform over the average number of SCM nodes; an ablation confirms TabPFN is biased toward simple causal explanations unlike gradient-boosted trees. (§1, p.2; §4.2, p.4; App. B.3.1, p.17) ^occam
- **two-module-attention**: The transformer encodes each feature-vector-plus-label as a token; self-attention is split into two weight-sharing modules — self-attention among training examples and cross-attention from test to training examples — making the input a permutation-invariant set. (§2 "Architecture," p.3; Fig. 1b; App. E.2, p.29) ^two-module-attention
- **flexible-features**: To handle differing feature counts, the feature dimension is drawn uniformly up to 100 during training and datasets are zero-padded to the max $K$, scaling padded features by $K/k$ to preserve magnitude. (§3, p.3; App. E.2 "Flexible Encoder," p.29) ^flexible-features
- **preprocessing**: Inputs are normalized to zero mean/unit variance with power (Yeo–Johnson) scaling for exponential data; missing values are replaced with zero (no special NaN handling); categorical features are assigned to a random fraction of columns (20% probability) during prior-fitting; correlated features arise via blockwise feature sampling. (App. C.2.1–C.2.5, pp.27–28) ^preprocessing
- **no-tuning**: TabPFN "needs no hyperparameter tuning"; being fully Bayesian over the prior's hyperparameters, the PPD "jointly integrates over this space and the respective model weights," requiring no cross-validation or model selection. (Abstract; §1, p.2; §4.1, p.4) ^no-tuning
- **training-scale**: The single TabPFN used for all experiments is a 12-layer transformer (embedding 512, feed-forward 1024, 4 heads, 25.82M parameters) trained for 18,000 steps of 512 synthetic datasets each ($\approx$ 9.2M synthetic datasets), taking 20 h on 8 RTX 2080 Ti GPUs; each synthetic dataset had fixed size 1024. (§3, p.3; App. E.1, E.3, pp.29–30) ^training-scale
- **size-limits**: TabPFN 2023 supports $\leq 1{,}000$ training examples, $\leq 100$ purely numerical features without missing values, and $\leq 10$ classes; beyond these limits "the precise TabPFN that we fitted cannot work." (Abstract; §1, p.2; App. A, p.15) ^size-limits
- **speed**: TabPFN predicts in under a second, tying AutoML systems that tune for one hour — 230× faster on CPU, 5,700× on GPU. Efficiency partly comes from shrinking the attention matrix from $(n+m)^2$ to $n^2 + n\cdot m$ (n train, m test); the 32-member permutation ensemble takes 0.62 s on GPU. The paper describes no KV/state-caching mechanism — speed comes from the single forward pass plus reduced attention cost. (Abstract; Table 1, p.8; §5.2, pp.8–9; App. C.2.6, p.28) ^speed
- **benchmark**: On 18 numerical OpenML-CC18 datasets (60-min budget), TabPFN reaches mean AUC OVO 0.934 vs LightGBM 0.920 / CatBoost 0.924 / XGBoost 0.924 / Auto-sklearn 2.0 0.929 / AutoGluon 0.930, the best individual mean rank (2.94); the "TabPFN + AutoGluon" ensemble is best overall. (Table 1, p.8; §5.2, p.9) ^benchmark
- **generalization**: Though trained only on synthetic datasets $\leq 1{,}024$ samples, TabPFN generalizes beyond training sample sizes, extrapolating to 5,000 samples; its errors are "quite uncorrelated" to existing methods, making it an ideal ensembling candidate. (§5.2 "Model Generalization," p.9; Fig. 10) ^generalization
- **scm-beats-bnn**: An ablation (Table 4, p.20) shows the SCM prior (ROC AUC 0.881) beats the BNN prior (0.865), and mixing them (0.883) barely changes the result — the novel SCM prior is the key contribution. (App. B, Table 4, p.20) ^scm-beats-bnn
- **limitations-2023**: Stated limitations — development focused on purely numerical datasets without missing values, so performance is "generally worse" on datasets with categorical features and/or missing values; the prior "did not consider the existence of many uninformative features," "leading to performance degradation when such features are added"; and because TabPFN fits and predicts at once, baseline models are "often faster than TabPFN in terms of pure inference time." (§7 Conclusions, p.10) ^limitations-2023

## Notes

- Attention scales quadratically in the number of inputs, so inference on >100,000 samples is hard on consumer GPUs (App. A, p.15). Builds directly on the PFN framework of Müller et al. 2022, whose predecessor was limited to 30 samples / balanced binary / 60 features.
