# Fraud Detection Feature Store

## Overview

Build a production-grade feature store using Feast for a fraud detection system. The project covers offline feature computation from batch sources, online feature serving for real-time inference, feature versioning, and point-in-time correct feature retrieval for training data generation.

## Learning Objectives

- Understand feature store architecture and the separation of offline/online stores
- Define entities, feature views, and feature services in Feast
- Implement batch feature computation for transaction, user, and aggregation features
- Materialize features from offline to online stores
- Perform point-in-time correct feature retrieval to prevent data leakage
- Serve features via a FastAPI endpoint for real-time inference
- Generate synthetic fraud detection data with realistic patterns

## Project Description

You are building a feature store for a fraud detection ML system. The system must:

1. **Define feature schemas** — Create Feast entities, feature views, and feature services for fraud-related features
2. **Compute transaction features** — Amount statistics, frequency, and velocity features per user
3. **Compute user features** — Account age, historical spending patterns, and risk indicators
4. **Compute aggregation features** — Time-windowed rolling statistics (1h, 24h, 7d windows)
5. **Materialize features** — Push computed features from offline to online store for serving
6. **Serve features online** — FastAPI endpoint that retrieves features and returns fraud predictions
7. **Generate training data** — Point-in-time correct historical feature retrieval for model training

## Architecture

```
feature_store/
├── feature_repo/
│   ├── feature_definitions.py   # Feast feature views, entities, feature services
│   ├── data_sources.py          # Data source definitions (FileSource, batch)
│   └── feature_store.yaml       # Feast repo configuration
├── features/
│   ├── transaction_features.py  # Transaction-based features
│   ├── user_features.py         # User profile features
│   └── aggregation_features.py  # Time-windowed aggregation features
├── materialization.py           # Feature materialization to online store
├── serving.py                   # FastAPI online feature serving
├── offline_retrieval.py         # Training data via point-in-time joins
└── data_generator.py            # Synthetic fraud data generation
```

## Implementation Tasks

### Phase 1: Data & Feature Definitions
- [ ] Implement synthetic fraud data generator with realistic transaction patterns
- [ ] Define Feast entities (user, transaction, merchant)
- [ ] Define data sources (FileSource for parquet files)
- [ ] Create feature views for transaction, user, and aggregation features
- [ ] Create a feature service combining all views for fraud detection

### Phase 2: Feature Computation
- [ ] Implement transaction features (amount mean/std/max, transaction count, velocity)
- [ ] Implement user features (account age, avg spend, days since last transaction)
- [ ] Implement aggregation features (1h, 24h, 7d rolling windows for amount and count)

### Phase 3: Online Serving
- [ ] Write materialization script to populate online store
- [ ] Build FastAPI endpoint that retrieves online features by entity key
- [ ] Integrate a simple fraud prediction model using served features

### Phase 4: Offline Retrieval
- [ ] Implement point-in-time correct joins for training data generation
- [ ] Generate a training dataset from historical features and labels
- [ ] Validate that no future data leaks into the training set

## Evaluation Criteria

- Feature views and entities register successfully with Feast
- Materialization populates the online store without errors
- Online serving returns correct feature vectors for given entity keys
- Point-in-time joins produce training data without temporal leakage
- Aggregation windows compute correctly across time boundaries
- Synthetic data has realistic fraud patterns (class imbalance, correlated features)
- All tests pass and cover core functionality

## Resources

- [Feast Documentation](https://docs.feast.dev/)
- [Feast Quickstart](https://docs.feast.dev/getting-started/quickstart)
- [Feature Store for ML (Hopsworks book)](https://www.featurestore.org/)
- [Point-in-Time Correctness Explained](https://docs.feast.dev/getting-started/concepts/point-in-time-joins)
- [Feature Stores: A Hierarchy of Needs](https://eugeneyan.com/writing/feature-stores/)
