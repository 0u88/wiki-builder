# Math Conventions

This section defines how mathematical notation is written in this wiki. Every concept article that contains math must follow these conventions. The goal is consistency across the whole wiki — not "the best possible notation in the abstract", but **one** notation chosen and applied uniformly.

The reference style is **Wasserman, _All of Statistics_** (2004), adapted for ML and computational research contexts. When in doubt, ask: "how would Wasserman write this?"

---

## Renderer

This wiki is read in **Obsidian with default MathJax 3** (no KaTeX, no custom preamble). Every example below has been chosen to render correctly under that setup. Do not use LaTeX commands that require external packages (`tikz-cd`, `physics`, `mathtools`, etc.) unless explicitly noted.

---

## Delimiters

| Use case | Syntax | Notes |
|---|---|---|
| Inline math | `$ ... $` | Never `\( ... \)`. Surround with normal spaces, not Chinese spaces. |
| Display math | `$$ ... $$` | Always on its own paragraph with a blank line above and below. Never inline. |
| Multi-line aligned | `$$\begin{aligned} ... \end{aligned}$$` | Use `aligned`, NOT bare `align` or `align*`. Obsidian will not render bare `align`. |
| Cases | `$$\begin{cases} ... \end{cases}$$` | Standard. |
| Matrices | `\begin{pmatrix} ... \end{pmatrix}` | Default to `pmatrix`. Use `bmatrix` only when brackets are semantically meaningful. |

**Spacing around display math:**

```markdown
The PPI estimator is defined as

$$
\hat\theta^{\mathrm{PPI}} = \frac{1}{N} \sum_{i=1}^N f(X_i) + \frac{1}{n} \sum_{i=1}^n \bigl(Y_i - f(X_i)\bigr).
$$

It satisfies the unbiasedness property...
```

Blank line above the `$$`, blank line below. No exceptions.

---

## Core notation (Wasserman convention)

### Probability and statistics

| Object | Notation | Example |
|---|---|---|
| Probability | `\mathbb{P}` | $\mathbb{P}(A)$, $\mathbb{P}(X \leq x)$ |
| Expectation | `\mathbb{E}` | $\mathbb{E}[X]$, $\mathbb{E}_{p}[f(X)]$ |
| Variance | `\mathrm{Var}` | $\mathrm{Var}(X)$ |
| Covariance | `\mathrm{Cov}` | $\mathrm{Cov}(X, Y)$ |
| Random variable | Capital italic | $X$, $Y$, $Z$ |
| Realization | Lowercase italic | $x$, $y$, $z$ |
| Random vector | Capital italic, NOT bold | $X = (X_1, \ldots, X_d)$ |
| Sample | $X_1, \ldots, X_n$ | iid implied unless stated |
| Estimator (random) | Hat on capital | $\hat\theta_n$, $\hat F_n$ |
| Parameter (true) | Plain Greek | $\theta$, $\mu$, $\sigma^2$ |
| True parameter (when ambiguous) | Star | $\theta^*$, $\theta_0$ |
| Indicator | `\mathbf{1}` | $\mathbf{1}\{X > 0\}$ |
| Distribution | $X \sim F$ | $X \sim N(\mu, \sigma^2)$ |
| Convergence in distribution | `\rightsquigarrow` | $\hat\theta_n \rightsquigarrow N(0, 1)$ — Wasserman's convention |
| Convergence in probability | `\xrightarrow{P}` | $\hat\theta_n \xrightarrow{P} \theta$ |
| Almost sure convergence | `\xrightarrow{\text{a.s.}}` | $\hat\theta_n \xrightarrow{\text{a.s.}} \theta$ |

### Sets and number systems

| Object | Notation |
|---|---|
| Reals | `\mathbb{R}` → $\mathbb{R}$ |
| Naturals | `\mathbb{N}` → $\mathbb{N}$ |
| Integers | `\mathbb{Z}` → $\mathbb{Z}$ |
| Sample space | `\mathcal{X}`, `\mathcal{Y}` → $\mathcal{X}, \mathcal{Y}$ |
| Sigma-algebra | `\mathcal{F}` → $\mathcal{F}$ |
| Hypothesis class / function space | `\mathcal{H}`, `\mathcal{F}` → $\mathcal{H}, \mathcal{F}$ |

### Vectors and matrices (ML convention layered on Wasserman)

Wasserman doesn't bold vectors. Modern ML usually does. We pick **bold for vectors and matrices** to match ML convention, since most of this wiki's ML content benefits from the visual distinction.

| Object | Notation | Example |
|---|---|---|
| Vector | `\mathbf{x}` | $\mathbf{x} \in \mathbb{R}^d$ |
| Matrix | `\mathbf{A}` (uppercase) | $\mathbf{A} \in \mathbb{R}^{n \times d}$ |
| Vector component | Plain italic with subscript | $x_i$, not $\mathbf{x}_i$ |
| Transpose | `^\top` | $\mathbf{A}^\top$, not `^T` or `^{\mathrm{T}}` |
| Inverse | `^{-1}` | $\mathbf{A}^{-1}$ |
| Inner product | `\langle \cdot, \cdot \rangle` | $\langle \mathbf{x}, \mathbf{y} \rangle$ |
| Norm | `\|\cdot\|` | $\|\mathbf{x}\|_2$ — use `\|`, not `\Vert` or `||` |

**Caveat**: when an article is purely about probability theory or measure theory and has no ML content, you may drop the bold and use $X$ for vectors (Wasserman's original style). State this in a one-line note at the top of the article: `> Notation: random vectors written without bold throughout.`

### Operators

These are the operators where students and LLMs most often write something almost-correct but stylistically wrong.

| Operator | Correct LaTeX | Renders as | Common mistakes to avoid |
|---|---|---|---|
| argmax | `\operatorname*{arg\,max}_{x}` | $\operatorname*{arg\,max}_{x}$ | Don't use `\arg\max` (no thin space, subscript wrong) |
| argmin | `\operatorname*{arg\,min}_{x}` | $\operatorname*{arg\,min}_{x}$ | Same |
| sup | `\sup_{x}` | $\sup_{x}$ | Built in |
| inf | `\inf_{x}` | $\inf_{x}$ | Built in |
| max | `\max_{x}` | $\max_{x}$ | Built in |
| min | `\min_{x}` | $\min_{x}$ | Built in |
| KL divergence | `D_{\mathrm{KL}}(p \,\|\, q)` | $D_{\mathrm{KL}}(p \,\|\, q)$ | Not `KL(p||q)`, not `\text{KL}` |
| Cross-entropy | `H(p, q)` or `H_{\mathrm{CE}}(p, q)` | $H(p, q)$ | |
| Entropy | `H(X)` or `H(p)` | $H(X)$ | |
| Mutual info | `I(X; Y)` | $I(X; Y)$ | Semicolon, not comma |
| Trace | `\mathrm{tr}` | $\mathrm{tr}(\mathbf{A})$ | Not `\text{tr}`, not `Tr` |
| Determinant | `\det` | $\det(\mathbf{A})$ | Built in |
| Rank | `\mathrm{rank}` | $\mathrm{rank}(\mathbf{A})$ | |
| Span | `\mathrm{span}` | $\mathrm{span}\{\mathbf{v}_1, \ldots\}$ | |
| Diag | `\mathrm{diag}` | $\mathrm{diag}(\lambda_1, \ldots, \lambda_d)$ | |
| Sign | `\mathrm{sign}` | $\mathrm{sign}(x)$ | |

**Why `\operatorname*` for argmax/argmin?** The star puts the subscript directly underneath in display mode (where it belongs), instead of to the lower-right. This is the Wasserman-style convention.

### Calculus and analysis

| Object | Notation | Example |
|---|---|---|
| Derivative | `\frac{d f}{d x}` | $\frac{df}{dx}$ |
| Partial | `\frac{\partial f}{\partial x}` | $\frac{\partial f}{\partial x}$ |
| Gradient | `\nabla` | $\nabla f(\mathbf{x})$ |
| Hessian | `\nabla^2` or `\mathbf{H}` | $\nabla^2 f(\mathbf{x})$ |
| Jacobian | `\mathbf{J}` | $\mathbf{J}_f(\mathbf{x})$ |
| Integral over set | `\int_{A}` | $\int_A f \, d\mu$ |
| Lebesgue measure | $d\mu$, $dx$ | use `\,` thin space before $d$ |
| Big-O | `O(\cdot)` or `\mathcal{O}(\cdot)` | $\mathcal{O}(n \log n)$ — pick one and stick to it; this wiki uses $\mathcal{O}$ |
| little-o | `o(\cdot)` | $o(n)$ |
| Big-Omega | `\Omega(\cdot)` | $\Omega(n)$ — context disambiguates from sample space |

### Optimization

| Object | Notation |
|---|---|
| Loss / objective | $L(\theta)$ or $\mathcal{L}(\theta)$ — use $\mathcal{L}$ when there's also a likelihood $L$ |
| Empirical loss | $\hat L_n(\theta) = \frac{1}{n} \sum_{i=1}^n \ell(\theta; X_i, Y_i)$ |
| Per-sample loss | $\ell(\theta; x, y)$ |
| Step size | $\eta$ |
| Iteration index | $t$ |
| Update rule | $\theta_{t+1} = \theta_t - \eta \nabla L(\theta_t)$ |

### Linear algebra

Mostly covered above. A few extras:

| Object | Notation |
|---|---|
| Identity matrix | $\mathbf{I}$ or $\mathbf{I}_d$ |
| Zero vector | $\mathbf{0}$ |
| Eigenvalues | $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_d$ |
| Eigenvectors | $\mathbf{v}_1, \ldots, \mathbf{v}_d$ |
| Singular values | $\sigma_1 \geq \sigma_2 \geq \cdots$ |

### Measure theory (only when needed)

For articles that genuinely require it. Most articles should not.

| Object | Notation |
|---|---|
| Probability space | $(\Omega, \mathcal{F}, \mathbb{P})$ |
| Measurable space | $(\mathcal{X}, \mathcal{B})$ |
| Sigma-algebra generated | $\sigma(\cdot)$ |
| Pushforward | $\mu = X_* \mathbb{P}$ |
| Radon-Nikodym | $\frac{d\mu}{d\nu}$ |

---

## Spacing rules

LaTeX spacing decisions that matter:

| Situation | Rule | Example |
|---|---|---|
| Before $d$ in integrals | `\,` thin space | $\int f(x) \, dx$ |
| After commas in tuples | normal space | $(x_1, x_2, x_3)$ |
| Around binary operators | none (LaTeX handles it) | $a + b$, not `a +\, b` |
| Inside `\|...\|` for KL | `\,\|\,` | $D_{\mathrm{KL}}(p \,\|\, q)$ |
| Between consecutive symbols | `\,` if visually crowded | $f(x)\,g(y)$ |

Avoid manual spacing (`\quad`, `\qquad`, `\hspace`) outside of tables and matrices. Trust LaTeX defaults.

---

## Brackets

Use auto-sizing **only** when the expression inside is genuinely tall (fractions, sums, integrals). For ordinary expressions, fixed brackets are cleaner.

| Situation | Use |
|---|---|
| Ordinary expressions | `(...)`, `[...]`, `\{...\}` |
| Around fractions, sums, integrals | `\bigl(...\bigr)`, `\Bigl(...\Bigr)`, or `\left(...\right)` |
| Set-builder | `\{x \in \mathcal{X} : f(x) > 0\}` — use `:`, not `\mid` or `|` |
| Conditional probability | `\mathbb{P}(A \mid B)` — use `\mid`, not `|`, gives correct spacing |

**Default to fixed-size brackets.** `\left( \right)` adds extra horizontal padding that often looks wrong. Reach for it only when you really need vertical scaling.

---

## Inline vs display: when to use which

- **Inline** ($...$): single symbols, short expressions, anything that reads naturally inside prose ("the estimator $\hat\theta_n$ converges...", "for all $\epsilon > 0$").
- **Display** ($$...$$): equations that the reader needs to parse carefully, definitions, theorems, anything with a fraction/sum/integral that would crowd a line of prose, and **always** for multi-line derivations.

Rule of thumb: if the expression contains $\sum$, $\int$, $\frac{}{}$, or has more than ~6 symbols, use display.

---

## What NOT to do

A blacklist of things that look almost right but aren't:

1. **`E[X]` for expectation** → use `\mathbb{E}[X]`
2. **`P(A)` for probability** → use `\mathbb{P}(A)`
3. **Bare `\begin{align}` outside `$$...$$`** → Obsidian won't render it. Always `$$\begin{aligned}...\end{aligned}$$`.
4. **`\frac{1}{2}` in inline math** → use `1/2` to keep line height stable. Reserve `\frac` for display.
5. **`x^T` or `x^{T}` for transpose** → use `\mathbf{x}^\top`
6. **`||x||` or `\Vert x \Vert`** → use `\|x\|`
7. **`KL(p||q)`** → use `D_{\mathrm{KL}}(p \,\|\, q)`
8. **`\arg\max`** → use `\operatorname*{arg\,max}`
9. **`<x, y>` for inner product** → use `\langle x, y \rangle`
10. **`\text{some words}` in math mode for operator names** → use `\mathrm{}` for short operator names, `\operatorname{}` if you want LaTeX to handle the spacing
11. **Mixing $...$ and \(...\) in the same article** → only use $...$
12. **Inline math touching Chinese characters with no space** → not applicable here (English-only wiki), but worth knowing if the wiki ever goes bilingual
13. **Hand-rolled fractions like `1\over2`** → always use `\frac{}{}` syntax
14. **Variable named `e` for both Euler's constant and an error term** → disambiguate: use $\mathrm{e}$ for Euler's constant if it appears in the same article as an error variable
15. **`$\sim$3` for "approximately 3"** → use `${\sim}3$`. Writing `$\sim$` as a standalone math block followed immediately by a number breaks Obsidian's MathJax parser — the closing `$` of `\sim` and the opening `$` of adjacent text create ambiguous delimiter boundaries. Always merge the `\sim` and the number into one math block: `${\sim}3$`, `${\sim}50$ km`, `${\sim}15°$`.

---

## When in doubt

Ask: **"Would Wasserman write it this way in _All of Statistics_?"** If you're not sure, default to the simpler / more conventional choice. A consistently slightly-suboptimal notation is better than a randomly-mixed "best" notation.
