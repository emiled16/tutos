# ML Pipeline Orchestrator with Apache Airflow

## Overview

Build an end-to-end ML pipeline using Apache Airflow that orchestrates the full model lifecycle: data ingestion, data validation, feature engineering, model training, evaluation, and model registration. The project teaches DAG design patterns, custom operators, production best practices, and monitoring.

## Learning Objectives

- Understand DAG (Directed Acyclic Graph) concepts and how Airflow schedules work
- Build custom operators, sensors, and hooks for ML-specific tasks
- Implement data validation and quality checks as pipeline steps
- Design idempotent tasks that can be safely retried and backfilled
- Configure proper error handling, retries, SLAs, and alerting
- Manage connections, variables, and secrets in Airflow
- Pass data between tasks using XComs and TaskFlow API

## Project Description

You are building an ML platform team's pipeline infrastructure. The system must handle:

1. **Data Ingestion** — Pull data from APIs, S3, and databases on a schedule
2. **Data Validation** — Validate schema, check for drift, ensure data quality
3. **Feature Engineering** — Transform raw data into model-ready features
4. **Model Training** — Train ML models with configurable hyperparameters
5. **Model Evaluation** — Evaluate against baseline metrics and thresholds
6. **Model Registration** — Register approved models in a model registry

## Architecture

```
src/airflow/
├── dags/
│   ├── ml_pipeline_dag.py       # Main end-to-end ML pipeline DAG
│   └── data_ingestion_dag.py    # Standalone data ingestion DAG
├── operators/
│   ├── training_operator.py     # Custom operator for model training
│   └── validation_operator.py   # Custom operator for data validation
├── hooks/
│   └── model_registry_hook.py   # Hook for model registry API
├── sensors/
│   └── data_sensor.py           # Sensor for data availability
└── utils/
    ├── config.py                # Pipeline configuration management
    └── notifications.py         # Slack/email notification helpers
```

## Implementation Tasks

### Phase 1: DAG Design
- [ ] Define the main ML pipeline DAG with correct task dependencies
- [ ] Configure scheduling, retries, SLAs, and timeouts
- [ ] Implement the data ingestion DAG with multiple data sources
- [ ] Set up task groups for logical organization

### Phase 2: Custom Components
- [ ] Build a custom `ModelTrainingOperator` with parameter passing
- [ ] Build a custom `DataValidationOperator` with quality checks
- [ ] Implement `ModelRegistryHook` for model storage interaction
- [ ] Implement `DataAvailabilitySensor` with configurable poke intervals

### Phase 3: Pipeline Utilities
- [ ] Create configuration management for environment-specific settings
- [ ] Implement Slack and email notification callbacks
- [ ] Set up XCom patterns for data passing between tasks

### Phase 4: Testing
- [ ] Validate DAG structure (no import errors, no cycles)
- [ ] Test custom operators with mocked dependencies
- [ ] Test notification callbacks

## Evaluation Criteria

- DAGs load without import errors and have no cycles
- Custom operators properly inherit from BaseOperator and implement execute()
- Sensors correctly implement poke() with appropriate return types
- Hooks manage connections via Airflow's connection system
- Tasks are idempotent (safe to retry and backfill)
- Error handling and notifications are properly configured
- XCom usage follows best practices (small data only)

## Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Astronomer Guides](https://docs.astronomer.io/learn)
- [TaskFlow API Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html)
