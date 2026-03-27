# ML Model A/B Testing Platform

## Overview

Build a statistical A/B testing framework that compares two ML recommendation models using proper statistical methods. The platform supports both frequentist and Bayesian approaches, sequential testing for early stopping, and automated report generation.

## Learning Objectives

- Understand hypothesis testing fundamentals (null/alternative hypotheses, Type I/II errors)
- Implement frequentist statistical tests (t-test, chi-squared, Mann-Whitney U)
- Implement Bayesian A/B testing with Beta-Binomial conjugate models
- Calculate sample sizes for desired statistical power
- Apply Sequential Probability Ratio Test (SPRT) for early stopping
- Compute effect sizes (Cohen's d) and confidence intervals
- Generate actionable experiment reports with visualizations

## Project Description

You are building an A/B testing platform for an ML team that regularly deploys new recommendation models. The platform must:

1. **Configure experiments** — Define control/treatment groups, primary/secondary metrics, and test duration
2. **Run statistical tests** — Compare metrics between groups using appropriate statistical tests
3. **Support Bayesian analysis** — Compute posterior distributions and probability of each variant being best
4. **Calculate sample sizes** — Determine required sample sizes before running experiments
5. **Enable early stopping** — Use sequential testing to stop experiments early when results are conclusive
6. **Generate reports** — Produce HTML/JSON reports with charts and statistical summaries

## Architecture

```
ab_testing/
├── experiment.py      # Experiment configuration and lifecycle management
├── statistics.py      # Frequentist statistical tests
├── bayesian.py        # Bayesian A/B testing (Beta-Binomial)
├── sample_size.py     # Power analysis and sample size calculation
├── sequential.py      # Sequential testing (SPRT)
├── reporter.py        # Report generation (HTML/JSON + visualizations)
└── simulator.py       # Data simulation for testing the framework
```

## Implementation Tasks

### Phase 1: Core Statistics
- [ ] Implement `Experiment` dataclass with configuration fields
- [ ] Implement Welch's t-test for continuous metrics
- [ ] Implement chi-squared test for proportions
- [ ] Implement Mann-Whitney U test for non-normal distributions
- [ ] Compute confidence intervals and effect sizes

### Phase 2: Bayesian Methods
- [ ] Implement Beta-Binomial model for conversion rates
- [ ] Compute posterior distributions from observed data
- [ ] Calculate probability of each variant being best via Monte Carlo
- [ ] Implement credible intervals

### Phase 3: Experiment Design
- [ ] Implement sample size calculator for t-test and proportions
- [ ] Support minimum detectable effect specification
- [ ] Implement SPRT for sequential testing with early stopping boundaries

### Phase 4: Reporting & Simulation
- [ ] Build data simulator with configurable effect sizes
- [ ] Generate HTML reports with matplotlib/plotly visualizations
- [ ] Generate JSON summaries for programmatic consumption

## Evaluation Criteria

- Statistical tests return correct p-values (validated against scipy)
- Bayesian posterior converges to known parameters with sufficient data
- Sample size calculator matches analytical formulas
- SPRT correctly stops early for large effect sizes
- Reports include all relevant statistics and visualizations
- Code handles edge cases (zero variance, empty groups, ties)

## Resources

- [Evan Miller's A/B Testing Guide](https://www.evanmiller.org/ab-testing/)
- [Bayesian A/B Testing at VWO](https://vwo.com/downloads/VWO_SmartStats_technical_whitepaper.pdf)
- [Sequential Testing (SPRT)](https://en.wikipedia.org/wiki/Sequential_probability_ratio_test)
- [scipy.stats documentation](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Practical Statistics for Data Scientists (O'Reilly)](https://www.oreilly.com/library/view/practical-statistics-for/9781492072935/)
