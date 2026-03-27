# ML Data Quality Guardian

## Overview

Build a comprehensive data quality framework using Great Expectations to ensure data quality at every stage of an ML pipeline. Create custom expectations for ML-specific checks including distribution validation, target leakage detection, and class balance verification.

## Learning Objectives

- Understand data quality dimensions and their impact on ML models
- Configure Great Expectations Data Context, data sources, and stores
- Build expectation suites for raw data, feature data, and prediction outputs
- Develop custom expectations for ML-specific validation (distribution shifts, correlations)
- Create checkpoints that run validation at pipeline stages
- Integrate data quality checks into an ML pipeline workflow
- Generate and interpret Data Docs for quality reporting

## Project Description

You are building a data quality framework for an ML pipeline that processes tabular data. The framework must:

1. **Validate raw data** — Check schema, completeness, value ranges, and uniqueness constraints
2. **Validate features** — Check distributions, correlations, and detect target leakage
3. **Validate predictions** — Check output format, probability ranges, and class balance
4. **Custom expectations** — Implement ML-specific expectations (KS test, PSI, correlation bounds)
5. **Pipeline integration** — Provide helpers that run validation at each pipeline stage
6. **Generate test data** — Create datasets with intentional quality issues for testing

## Architecture

```
great_expectations/
├── context_setup.py                 # GE context configuration
├── expectations/
│   ├── schema_expectations.py       # Custom schema validation expectations
│   ├── distribution_expectations.py # Distribution check expectations (KS, PSI)
│   └── ml_expectations.py           # ML-specific expectations
├── checkpoints/
│   ├── data_checkpoint.py           # Raw data validation checkpoint
│   ├── feature_checkpoint.py        # Feature validation checkpoint
│   └── prediction_checkpoint.py     # Prediction output validation checkpoint
├── suites/
│   ├── raw_data_suite.py            # Expectation suite for raw data
│   └── feature_suite.py             # Expectation suite for feature data
├── pipeline_integration.py          # Integration helpers for ML pipeline
└── data_generator.py                # Test dataset generator
```

## Implementation Tasks

### Phase 1: Context & Suite Setup
- [ ] Configure Great Expectations Data Context with file-based stores
- [ ] Build raw data expectation suite (schema, completeness, ranges)
- [ ] Build feature data expectation suite (distributions, correlations)

### Phase 2: Custom Expectations
- [ ] Implement schema validation expectations (column types, required columns)
- [ ] Implement distribution expectations (KS test for drift, PSI for stability)
- [ ] Implement ML expectations (target leakage via correlation, class balance ratio)

### Phase 3: Checkpoints
- [ ] Create raw data checkpoint that validates incoming data
- [ ] Create feature checkpoint that validates transformed features
- [ ] Create prediction checkpoint that validates model outputs

### Phase 4: Pipeline Integration
- [ ] Build pipeline integration helpers that run checkpoints at each stage
- [ ] Implement validation result aggregation and reporting
- [ ] Create a data generator with configurable quality issues for testing

## Evaluation Criteria

- Custom expectations correctly detect the quality issues they target
- KS test expectation properly identifies distribution shifts
- PSI expectation flags population stability changes
- Target leakage detector catches high feature-target correlations
- Checkpoints pass on clean data and fail on corrupted data
- Pipeline integration correctly gates pipeline stages on data quality
- All tests pass and cover both pass and fail scenarios

## Resources

- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [Custom Expectations Guide](https://docs.greatexpectations.io/docs/guides/expectations/creating_custom_expectations/overview)
- [Data Quality Fundamentals (O'Reilly)](https://www.oreilly.com/library/view/data-quality-fundamentals/9781098112035/)
- [PSI (Population Stability Index)](https://scholarworks.wmich.edu/dissertations/3208/)
- [Testing Data Pipelines (Martin Fowler)](https://martinfowler.com/articles/data-monolith-to-mesh.html)
