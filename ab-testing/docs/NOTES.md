# A/B Testing — Theory & Notes

## Hypothesis Testing Fundamentals

A/B testing is rooted in **hypothesis testing**: we compare a control group (A) against a treatment group (B) to determine whether an observed difference is statistically meaningful or due to chance.

- **Null hypothesis (H₀):** There is no difference between A and B (μ_A = μ_B)
- **Alternative hypothesis (H₁):** There is a difference (μ_A ≠ μ_B for two-sided)

### Type I and Type II Errors

| | H₀ True | H₀ False |
|---|---|---|
| **Reject H₀** | Type I Error (α) | Correct (Power) |
| **Fail to Reject** | Correct | Type II Error (β) |

- **Type I error (α):** False positive — concluding there is an effect when there isn't. Conventionally α = 0.05.
- **Type II error (β):** False negative — failing to detect a real effect. Power = 1 - β, typically target 0.80.
- There is a direct tradeoff: lowering α increases β (and vice versa) for a fixed sample size.

### P-Values

The p-value is the probability of observing a result at least as extreme as the one measured, **assuming the null hypothesis is true**.

- p < α → reject H₀ (result is "statistically significant")
- p-value is NOT the probability that H₀ is true
- p-value is NOT the probability of the result being due to chance
- Small p-values don't imply large or meaningful effects

### Confidence Intervals

A 95% confidence interval means: if we repeated the experiment many times, 95% of the computed intervals would contain the true parameter. It provides information about both the magnitude and precision of an estimate.

## Statistical Tests

### Welch's t-test
- Compares means of two independent samples
- Does NOT assume equal variances (unlike Student's t-test)
- Assumes approximately normal distributions (robust for large n via CLT)
- Formula: t = (x̄₁ - x̄₂) / √(s₁²/n₁ + s₂²/n₂)

### Chi-squared test
- Compares proportions (e.g., conversion rates)
- Uses contingency table of observed vs expected frequencies
- Assumes sufficient expected cell counts (≥ 5)

### Mann-Whitney U test
- Non-parametric alternative to t-test
- Compares distributions (ranks) rather than means
- Useful when data is ordinal or heavily skewed
- Makes no distributional assumptions

## Effect Size — Cohen's d

Cohen's d quantifies the magnitude of the difference in standard deviation units:

d = (x̄₁ - x̄₂) / s_pooled

| d | Interpretation |
|---|---|
| 0.2 | Small |
| 0.5 | Medium |
| 0.8 | Large |

**Practical significance vs statistical significance:** A huge sample can make a tiny difference "statistically significant." Always report effect sizes alongside p-values.

## Bayesian A/B Testing

### Beta-Binomial Model

For conversion rate testing (binary outcomes):

- **Prior:** Beta(α₀, β₀) — typically Beta(1, 1) = Uniform
- **Likelihood:** Binomial(n, p)
- **Posterior:** Beta(α₀ + successes, β₀ + failures)

The Beta distribution is the conjugate prior for the Binomial likelihood, giving a closed-form posterior.

### Probability of Being Best

Draw samples from each variant's posterior distribution and compute the fraction of times each variant has the highest sampled value. This directly answers: "What is the probability that B is better than A?"

### Bayesian vs Frequentist

| Aspect | Frequentist | Bayesian |
|---|---|---|
| Interpretation | Long-run frequency | Degree of belief |
| Parameters | Fixed but unknown | Random variables |
| Result | p-value, CI | Posterior distribution |
| Sample size | Fixed in advance | Can update continuously |
| Multiple testing | Requires correction | Naturally handled |
| Early stopping | Inflates Type I error | Valid at any point |

## Sample Size Calculation (Power Analysis)

To determine sample size per group, you need:
- **α** (significance level, typically 0.05)
- **β** (Type II error rate, typically 0.20 → power = 0.80)
- **MDE** (Minimum Detectable Effect — smallest effect worth detecting)
- **Baseline rate** (for proportions) or **standard deviation** (for means)

Formula (two-sample t-test):
n = (z_{α/2} + z_β)² × 2σ² / δ²

where δ = MDE, σ = population standard deviation.

## Sequential Testing (SPRT)

The Sequential Probability Ratio Test allows checking results as data arrives, with controlled Type I error.

### How SPRT Works

1. Define two boundaries: upper (reject H₀) and lower (accept H₀)
2. After each observation, compute the log-likelihood ratio
3. If ratio crosses upper boundary → stop, declare significant
4. If ratio crosses lower boundary → stop, declare not significant
5. Otherwise → continue collecting data

Boundaries: A = (1 - β) / α, B = β / (1 - α)

### Why naive peeking is dangerous

If you run a fixed-horizon test and peek at results repeatedly, each peek is an independent chance to get a false positive. After 5 peeks at α = 0.05, the effective false positive rate can exceed 14%.

## Multiple Testing Correction

When running multiple tests simultaneously (e.g., testing several metrics):

- **Bonferroni correction:** Divide α by the number of tests. Simple but conservative.
- **Holm-Bonferroni:** Step-down procedure. Less conservative than Bonferroni.
- **Benjamini-Hochberg (FDR):** Controls the false discovery rate rather than family-wise error rate.

## Simpson's Paradox

A trend that appears in several groups of data can reverse when the groups are combined. This is critical in A/B testing:

- Example: Treatment B has higher conversion in both mobile AND desktop segments, but A has higher conversion overall (because A had more traffic from the higher-converting segment).
- Always segment results and check for confounders.

## Common Pitfalls

1. **Peeking at results** — Checking significance repeatedly inflates false positives (use sequential testing instead)
2. **Underpowered tests** — Running with too few samples to detect realistic effects
3. **Multiple testing without correction** — Testing many metrics without adjusting significance thresholds
4. **Ignoring practical significance** — A statistically significant but tiny effect may not be worth the engineering cost
5. **Selection bias** — Non-random assignment to groups (e.g., assigning by user ID modulo can correlate with behavior)
6. **Novelty/primacy effects** — Users may react differently to a new experience temporarily
7. **Network effects** — Users in treatment may influence users in control (interference)

## Key Terminology

- **Control group:** The baseline (existing model/experience)
- **Treatment group:** The variant being tested
- **Statistical power:** Probability of detecting a true effect (1 - β)
- **Minimum Detectable Effect (MDE):** Smallest effect size the test is designed to detect
- **Credible interval (Bayesian):** Interval containing the parameter with specified posterior probability
- **Posterior distribution:** Updated belief about a parameter after observing data
- **Likelihood ratio:** Ratio of data probability under H₁ vs H₀
- **Effect size:** Standardized measure of the magnitude of a difference
