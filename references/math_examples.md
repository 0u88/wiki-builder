# Math Examples — Golden Reference

This file contains worked examples of how mathematical writing should look in this wiki. When writing a math-heavy concept article, **read this file first and imitate its style**. Examples are more reliable than rules.

The conventions encoded here are documented in `math_conventions.md`. This file is the "show, don't tell" companion.

---

## Example 1: A definition with inline math

The **sample mean** of an iid sample $X_1, \ldots, X_n$ is defined as

$$
\bar X_n = \frac{1}{n} \sum_{i=1}^n X_i.
$$

If $\mathbb{E}[X_1] = \mu$ and $\mathrm{Var}(X_1) = \sigma^2 < \infty$, then $\mathbb{E}[\bar X_n] = \mu$ and $\mathrm{Var}(\bar X_n) = \sigma^2 / n$.

**What this example shows:**
- Lead with the term in bold, then the definition.
- Single short formula → display math, not inline.
- Property statements that are short and parallel → inline math.
- $\mathbb{E}$, $\mathbb{V}$ for expectation and variance (Wasserman style).

---

## Example 2: A theorem statement

**Theorem (Central Limit Theorem).** Let $X_1, \ldots, X_n$ be iid with $\mathbb{E}[X_1] = \mu$ and $\mathrm{Var}(X_1) = \sigma^2 \in (0, \infty)$. Then

$$
\sqrt{n} \, (\bar X_n - \mu) \rightsquigarrow N(0, \sigma^2).
$$

Equivalently,

$$
\frac{\bar X_n - \mu}{\sigma / \sqrt{n}} \rightsquigarrow N(0, 1).
$$

**What this example shows:**
- Theorems get a bold lead-in, name in parentheses.
- $\rightsquigarrow$ for convergence in distribution (Wasserman's symbol).
- Two equivalent statements stacked as separate display equations, not crammed into `aligned`.
- Thin space `\,` between $\sqrt{n}$ and the parenthesis to avoid visual collision.

---

## Example 3: A multi-line derivation

To show that the sample mean is unbiased:

$$
\begin{aligned}
\mathbb{E}[\bar X_n]
&= \mathbb{E}\!\left[\frac{1}{n} \sum_{i=1}^n X_i\right] \\
&= \frac{1}{n} \sum_{i=1}^n \mathbb{E}[X_i] \\
&= \frac{1}{n} \cdot n \mu \\
&= \mu.
\end{aligned}
$$

**What this example shows:**
- `aligned` inside `$$...$$`, not bare `align`.
- Each line introduced with `&=` for alignment on the equals sign.
- `\!` negative thin space between $\mathbb{E}$ and the bracket — small touch but stops the bracket from looking detached.
- `\left[ ... \right]` only when the contents are tall (here: a sum with limits).
- Steps are atomic: one transformation per line.
- End with a period.

---

## Example 4: An estimator with a hat

The **Prediction-Powered Inference** (PPI) estimator combines a small labeled sample $(X_i, Y_i)_{i=1}^n$ with a large unlabeled pool $(\tilde X_j)_{j=1}^N$ and a predictive model $f : \mathcal{X} \to \mathbb{R}$:

$$
\hat\theta_n^{\mathrm{PPI}} = \underbrace{\frac{1}{N} \sum_{j=1}^N f(\tilde X_j)}_{\text{biased ML estimate}} + \underbrace{\frac{1}{n} \sum_{i=1}^n \bigl(Y_i - f(X_i)\bigr)}_{\text{rectifier (debiasing term)}}.
$$

Under iid sampling, $\mathbb{E}[\hat\theta_n^{\mathrm{PPI}}] = \mathbb{E}[Y]$ regardless of the accuracy of $f$.

**What this example shows:**
- Hat on the estimator: $\hat\theta$.
- Superscript `\mathrm{PPI}` for the variant name (not bold, not italic — it's a label, not a variable).
- `\underbrace{}_{\text{...}}` for annotating parts of a formula. Use sparingly — once or twice per article max.
- `\bigl( ... \bigr)` for medium-tall brackets. Cleaner than `\left( \right)` for this size.
- Mixing notation: $X_i$ for labeled, $\tilde X_j$ for unlabeled, $f(X_i)$ for the prediction.
- Statement of the key property in the next sentence, with inline math.

---

## Example 5: A loss function and gradient update

For a parameterized model $f_\theta : \mathcal{X} \to \mathcal{Y}$ and a per-sample loss $\ell : \mathcal{Y} \times \mathcal{Y} \to \mathbb{R}_{\geq 0}$, the **empirical risk** is

$$
\hat L_n(\theta) = \frac{1}{n} \sum_{i=1}^n \ell\bigl(f_\theta(X_i), Y_i\bigr).
$$

Gradient descent updates $\theta$ via

$$
\theta_{t+1} = \theta_t - \eta_t \, \nabla_\theta \hat L_n(\theta_t),
$$

where $\eta_t > 0$ is the **step size** at iteration $t$.

**What this example shows:**
- $\hat L_n$ for empirical (sample-size-indexed) quantities.
- Gradient with explicit subscript $\nabla_\theta$ when the variable being differentiated could be ambiguous.
- $\eta_t$ for step size at time $t$ — Wasserman/ML standard.
- Use $\mathbb{R}_{\geq 0}$ for non-negative reals; don't write $\mathbb{R}^+$ (ambiguous about whether $0$ is included).

---

## Example 6: A hypothesis test

To test $H_0 : \mu = \mu_0$ versus $H_1 : \mu \neq \mu_0$ at level $\alpha$, the **Wald test** uses the test statistic

$$
W = \frac{\hat\theta_n - \mu_0}{\hat{\mathrm{se}}(\hat\theta_n)},
$$

where $\hat{\mathrm{se}}$ is the estimated standard error. Under $H_0$, $W \rightsquigarrow N(0, 1)$, so we reject $H_0$ when $|W| > z_{\alpha/2}$.

**What this example shows:**
- Hypotheses with subscripted $H_0$, $H_1$.
- $\hat{\mathrm{se}}$ for "estimated standard error" — the $\mathrm{se}$ is an operator name (not italic), the hat indicates it's an estimate.
- $z_{\alpha/2}$ for the standard normal quantile.
- Single-bar absolute value $|W|$ — fixed-size brackets, not `\left| \right|`.

---

## Example 7: An optimization problem

The **constrained MLE** for $\theta$ subject to $g(\theta) \leq 0$ is

$$
\hat\theta_n = \operatorname*{arg\,max}_{\theta \in \Theta : g(\theta) \leq 0} \, \ell_n(\theta),
$$

where $\ell_n(\theta) = \sum_{i=1}^n \log p_\theta(X_i)$ is the log-likelihood.

**What this example shows:**
- `\operatorname*{arg\,max}` puts the constraint underneath the operator in display mode.
- Constraint set in subscript.
- Thin space `\,` between the operator and the function being maximized.
- Definitional aside introduced with "where".

---

## Example 8: A measure-theoretic statement (when needed)

Let $(\Omega, \mathcal{F}, \mathbb{P})$ be a probability space and $X : \Omega \to \mathbb{R}$ a random variable. The **distribution** of $X$ is the pushforward measure $\mu_X = X_* \mathbb{P}$ on $(\mathbb{R}, \mathcal{B})$, defined by

$$
\mu_X(B) = \mathbb{P}(X^{-1}(B)) = \mathbb{P}(\{X \in B\})
$$

for every Borel set $B \in \mathcal{B}$.

> Notation: this article uses measure-theoretic conventions. Random variables are not bolded and inner products are not used.

**What this example shows:**
- `(\Omega, \mathcal{F}, \mathbb{P})` — the standard probability space tuple.
- $X_* \mathbb{P}$ for pushforward, with subscript-style asterisk.
- The notation note as a callout (`>`) at the end of the example. In a real article it would go at the top.

---

## Example 9: Inline math in flowing prose

The estimator $\hat\theta_n$ is **consistent** if $\hat\theta_n \xrightarrow{P} \theta$ as $n \to \infty$. It is **asymptotically normal** if there exist sequences $a_n, b_n$ such that $a_n(\hat\theta_n - b_n) \rightsquigarrow N(0, 1)$. Together, consistency and asymptotic normality with $b_n = \theta$ and $a_n = \sqrt{n}/\tau$ for some $\tau > 0$ give the standard $\sqrt{n}$-asymptotic theory.

**What this example shows:**
- Heavy use of inline math without crowding.
- Bold for definitional terms (`**consistent**`, `**asymptotically normal**`).
- Multiple convergence types in the same paragraph, each with the right symbol.
- $\sqrt{n}$ used inline without `\frac` (which would inflate the line).

---

## Example 10: A short proof sketch

**Proof sketch.** By the linearity of expectation,

$$
\mathbb{E}[\hat\theta_n^{\mathrm{PPI}}] = \mathbb{E}[f(\tilde X)] + \mathbb{E}[Y] - \mathbb{E}[f(X)] = \mathbb{E}[Y],
$$

where the second equality uses that $X$ and $\tilde X$ are identically distributed. The $f$-terms cancel exactly, regardless of how biased $f$ is. $\square$

**What this example shows:**
- "Proof sketch" or "Proof" in bold as a paragraph lead-in.
- Short inline reasoning collapsed into one display equation with a single justification sentence.
- $\square$ at the end for proof termination (alternative: `\blacksquare`).

---

## How to use this file

When writing a new math-heavy article:

1. Skim the examples above and find the one closest to what you're writing.
2. Copy its structural pattern: how it leads in, where it switches between inline and display, how it spaces things out.
3. Cross-check against `math_conventions.md` for any specific symbol you're unsure about.
4. After writing, re-read with **only** this file open and ask: "does my article look like it could fit in here?"

If it doesn't — if the visual rhythm feels different, the symbols don't match, the spacing is off — fix the article, not this file.
