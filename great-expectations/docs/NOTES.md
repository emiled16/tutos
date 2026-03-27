# Data Quality with Great Expectations — Theory & Notes

## Data Quality Dimensions

Data quality is multidimensional. The key dimensions for ML are:

### Completeness
Are all expected records and fields present?
- Missing values (nulls, NaNs)
- Missing rows (dropped records in a pipeline)
- Missing columns (schema changes upstream)

### Accuracy
Do the values correctly represent the real-world entities?
- Values within expected ranges (age > 0, probability ∈ [0,1])
- Categorical values from expected sets
- Referential integrity (foreign keys resolve)

### Consistency
Are values consistent across different representations and over time?
- Same entity has the same ID across tables
- Timestamps are in a consistent timezone
- Units are consistent (meters vs feet)

### Timeliness
Is the data available when needed and does it reflect the current state?
- Data freshness (how recently was it updated?)
- Lag between event occurrence and data availability
- Stale features in ML systems

### Uniqueness
Are there duplicate records where there shouldn't be?
- Primary key uniqueness
- Deduplication of event streams
- Entity resolution

## Great Expectations Architecture

### Data Context

The Data Context is the entry point for all GE operations. It manages:
- **Configuration** — Where expectations, validation results, and Data Docs are stored
- **Data Sources** — Connections to data (pandas, Spark, SQL)
- **Expectation Suites** — Collections of expectations
- **Checkpoints** — Executable validation pipelines

```python
context = gx.get_context(mode="file", project_root_dir="./gx")
```

### Stores

GE uses stores to persist artifacts:
- **Expectations Store** — Serialized expectation suites (JSON)
- **Validations Store** — Results of checkpoint runs
- **Evaluation Parameter Store** — Dynamic values used in expectations
- **Checkpoint Store** — Checkpoint configurations

### Data Docs

Auto-generated HTML documentation of expectations and validation results. Acts as a data quality dashboard.

## Expectations

An expectation is a verifiable assertion about data. GE provides 300+ built-in expectations.

### Common Expectations

| Expectation | Purpose |
|---|---|
| `expect_column_to_exist` | Column is present in the dataset |
| `expect_column_values_to_not_be_null` | No null values |
| `expect_column_values_to_be_between` | Values within a range |
| `expect_column_values_to_be_in_set` | Values from an allowed set |
| `expect_column_mean_to_be_between` | Mean within bounds |
| `expect_column_distinct_values_to_be_in_set` | Only expected categories |
| `expect_table_row_count_to_be_between` | Expected number of rows |

### Custom Expectations

You can create custom expectations by subclassing:

```python
class ExpectColumnKsTestPValueToBeAbove(ColumnAggregateExpectation):
    metric_dependencies = ("column.custom.ks_test_p_value",)
    success_keys = ("min_p_value",)
    ...
```

Custom expectations require:
1. A **metric** that computes the value from data
2. A **success condition** that determines pass/fail
3. **Rendering** for Data Docs display (optional but recommended)

## Checkpoints

A checkpoint bundles:
- One or more **batches** of data (from a data source)
- An **expectation suite** to validate against
- **Actions** to take on results (store results, send notifications, update Data Docs)

```python
checkpoint = context.add_or_update_checkpoint(
    name="raw_data_checkpoint",
    validations=[{
        "batch_request": batch_request,
        "expectation_suite_name": "raw_data_suite",
    }],
)
result = checkpoint.run()
```

### Validation Actions

- `StoreValidationResultAction` — Persist results
- `UpdateDataDocsAction` — Regenerate Data Docs
- `SlackNotificationAction` — Send Slack alerts on failure
- `EmailAction` — Send email notifications

## ML-Specific Data Quality

### Distribution Drift

Feature distributions can shift between training and serving. Common measures:

**Kolmogorov-Smirnov (KS) Test:**
- Compares two distributions by their maximum CDF difference
- p-value < threshold → distributions differ significantly
- Non-parametric, works for continuous features

**Population Stability Index (PSI):**
- Measures shift between reference and current distributions
- PSI = Σ (p_i - q_i) × ln(p_i / q_i)
- PSI < 0.1: no shift, 0.1-0.2: moderate, > 0.2: significant
- Works by binning continuous values and comparing proportions

### Target Leakage Detection

Target leakage occurs when a feature contains information derived from the target variable that wouldn't be available at prediction time.

Detection approaches:
- **High correlation with target** — Features with |correlation| > 0.95 are suspicious
- **Perfect or near-perfect predictive power** — A single feature that achieves AUC > 0.99
- **Temporal analysis** — Features that use future information

### Class Balance

For classification tasks, monitoring class distribution is critical:
- Training data should reflect expected production distribution
- Extreme imbalance (e.g., 99.9% / 0.1%) may need resampling
- Sudden shifts in class ratios can indicate data pipeline issues

### Feature Correlation

Monitoring feature-feature correlations helps detect:
- Redundant features (high correlation between features)
- Broken features (correlation drops to 0 when it should be non-zero)
- Multicollinearity issues for linear models

## Data Profiling

GE can automatically profile data to generate initial expectation suites:

```python
profiler = UserConfigurableProfiler(
    profile_dataset=batch,
    excluded_expectations=None,
    ignored_columns=None,
    value_set_threshold="few",
)
suite = profiler.build_suite()
```

Profiling produces a starting point, but expectations should always be refined manually based on domain knowledge.

## Data Contracts

A data contract is a formal agreement between data producers and consumers about:
- Schema (columns, types)
- Semantics (what values mean)
- Quality guarantees (freshness, completeness)
- SLAs (availability, latency)

Great Expectations can enforce the technical aspects of data contracts through expectation suites and checkpoints.

## Integration with Orchestrators

GE integrates with pipeline orchestrators to validate data at each stage:

| Orchestrator | Integration |
|---|---|
| Airflow | `GreatExpectationsOperator` |
| Dagster | `@asset` with GE validation |
| Prefect | GE tasks in flows |
| dbt | `dbt-expectations` package |

Typical pattern:
1. Validate raw data after ingestion
2. Validate features after transformation
3. Validate predictions before serving

## Best Practices

1. **Start with profiling, then refine** — Auto-profile to bootstrap suites, then tighten based on domain knowledge
2. **Validate at every pipeline boundary** — Raw data in, features out, predictions out
3. **Set meaningful thresholds** — Overly strict expectations create alert fatigue
4. **Version your expectation suites** — Track changes alongside code
5. **Include both structural and statistical checks** — Schema + distribution
6. **Test your expectations** — Write tests that verify expectations pass/fail correctly
7. **Monitor trends, not just pass/fail** — A metric slowly approaching a threshold is worth investigating

## Common Pitfalls

1. **Too many expectations** — Hundreds of expectations that are hard to maintain
2. **Too strict thresholds** — Frequent false alarms that get ignored
3. **Not testing custom expectations** — Custom expectations with bugs that silently pass bad data
4. **Ignoring partial failures** — Only checking if the whole suite passes, not individual expectations
5. **Static reference distributions** — Reference data that isn't updated as the data naturally evolves
6. **Skipping prediction validation** — Trusting model output without checking format and ranges

## Key Terminology

- **Expectation** — A verifiable assertion about data (e.g., column values not null)
- **Expectation Suite** — A collection of expectations for a dataset
- **Checkpoint** — An executable that validates data against a suite and takes actions
- **Data Context** — The central configuration object for Great Expectations
- **Batch** — A specific slice of data to validate
- **Validator** — Object that evaluates expectations against a batch
- **Data Docs** — Auto-generated HTML documentation of expectations and results
- **Store** — Backend for persisting expectations, results, and checkpoints
- **PSI** — Population Stability Index, measures distribution shift
- **KS test** — Kolmogorov-Smirnov test for comparing distributions
- **Data contract** — Formal agreement about data schema, semantics, and quality
