# Software-Defined ML Assets with Dagster

## Overview

Build a [Dagster](https://dagster.io/) pipeline using the software-defined assets paradigm to orchestrate a complete ML workflow. The pipeline covers data ingestion, feature engineering, model training, and evaluation — all expressed as declarative assets with proper dependency tracking, custom IO managers, daily partitions, sensors, and comprehensive testing.

This project teaches you to think about data pipelines as **asset graphs** rather than task sequences — declaring *what* outputs exist and how they depend on each other, rather than *when* steps run.

## Learning Objectives

- Model an ML workflow as a graph of software-defined assets
- Implement custom IO managers for Parquet and ML model serialization
- Use daily partitions to process data incrementally
- Build sensors that trigger pipelines on external events
- Create schedules for recurring pipeline execution
- Write unit tests for assets, IO managers, and sensors
- Configure resources for dependency injection and testability
- Understand the difference between asset-based and task-based orchestration

## Project Description

You will build a pipeline that:

1. **Ingests** raw data (simulated dataset), producing a `raw_data` asset
2. **Cleans** the data, producing a `cleaned_data` asset
3. **Engineers features** from cleaned data, producing `feature_table` and `feature_stats` assets
4. **Trains** a model on the features, producing a `trained_model` asset with `model_metrics`
5. **Evaluates** the model against a holdout set, producing `evaluation_report` and `model_comparison` assets
6. All assets are **daily-partitioned** to support incremental processing
7. A **sensor** monitors for new data files and triggers the pipeline
8. A **schedule** runs daily retraining automatically

## Architecture

```
┌──────────┐     ┌──────────────┐     ┌───────────────┐
│ raw_data │────▶│ cleaned_data │────▶│ feature_table │──┐
└──────────┘     └──────────────┘     └───────────────┘  │
                                      ┌───────────────┐  │
                                      │ feature_stats │◀─┘
                                      └───────────────┘  │
                                                         │
                                      ┌───────────────┐  │
                                      │ trained_model │◀─┘
                                      └───────┬───────┘
                                              │
                              ┌───────────────┼──────────────────┐
                              ▼                                  ▼
                    ┌──────────────────┐            ┌───────────────────┐
                    │  model_metrics   │            │ evaluation_report │
                    └──────────────────┘            └───────────────────┘
                                                             │
                                                             ▼
                                                   ┌──────────────────┐
                                                   │ model_comparison │
                                                   └──────────────────┘

IO Managers:                      Resources:
├── ParquetIOManager (DataFrames) ├── DatabaseResource
└── ModelIOManager (ML models)    └── (injected via Definitions)

Triggers:
├── NewDataSensor (watches for new files)
└── DailySchedule (cron-based retraining)
```

## Implementation Tasks

### Phase 1: Data Models & Resources
- [ ] Define the database resource for data access
- [ ] Configure Dagster Definitions with all resources

### Phase 2: IO Managers
- [ ] Implement ParquetIOManager for reading/writing DataFrames as Parquet files
- [ ] Implement ModelIOManager for serializing/deserializing ML model artifacts
- [ ] Configure asset-to-IO-manager mapping

### Phase 3: Assets
- [ ] Implement `raw_data` asset — load/generate raw dataset
- [ ] Implement `cleaned_data` asset — handle missing values, type casting, outliers
- [ ] Implement `feature_table` asset — derive ML features from cleaned data
- [ ] Implement `feature_stats` asset — compute feature distributions and statistics
- [ ] Implement `trained_model` asset — train a scikit-learn model on features
- [ ] Implement `model_metrics` asset — compute training metrics (loss curves, etc.)
- [ ] Implement `evaluation_report` asset — evaluate model on holdout data
- [ ] Implement `model_comparison` asset — compare current model against previous

### Phase 4: Partitions & Scheduling
- [ ] Define daily partitions for incremental data processing
- [ ] Apply partitions to relevant assets
- [ ] Create a daily schedule for automatic retraining

### Phase 5: Sensors
- [ ] Implement a sensor that watches for new data files
- [ ] Trigger pipeline runs when new data arrives

### Phase 6: Testing
- [ ] Write unit tests for each asset with mock inputs
- [ ] Test IO managers with temporary directories
- [ ] Test sensor evaluation logic

## Evaluation Criteria

- Asset dependency graph is correctly defined and materializable
- Custom IO managers correctly serialize/deserialize DataFrames and models
- Daily partitions enable incremental processing
- Sensor detects new data and triggers runs
- Assets produce meaningful outputs (not just pass-throughs)
- Tests verify asset logic in isolation using Dagster's testing utilities
- Definitions object successfully loads in `dagster dev`

## Resources

- [Dagster Documentation](https://docs.dagster.io/)
- [Software-Defined Assets Guide](https://docs.dagster.io/concepts/assets/software-defined-assets)
- [IO Managers](https://docs.dagster.io/concepts/io-management/io-managers)
- [Partitions](https://docs.dagster.io/concepts/partitions-schedules-sensors/partitions)
- [Sensors](https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors)
- [Testing Assets](https://docs.dagster.io/concepts/testing)
