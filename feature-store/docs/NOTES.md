# Feature Stores — Theory & Notes

## What Is a Feature Store?

A feature store is a centralized system for managing, storing, and serving ML features. It bridges the gap between data engineering and data science by providing a consistent, reusable, and versioned layer of feature data.

The core problem it solves: in production ML systems, features computed during training must match features served during inference — otherwise you get **training-serving skew**.

## Feature Store Architecture

### Offline Store

The offline store holds historical feature values, typically in a data warehouse or data lake (BigQuery, Redshift, S3/Parquet). It is optimized for:

- **Batch reads** — Large-scale historical feature retrieval for training
- **Point-in-time joins** — Joining features to training examples as of the event timestamp
- **Backfills** — Recomputing features over historical data

### Online Store

The online store holds the **latest** feature values for each entity, typically in a low-latency key-value store (Redis, DynamoDB, Bigtable). It is optimized for:

- **Low-latency lookups** — Single-digit millisecond reads for real-time inference
- **High throughput** — Serving thousands of requests per second
- **Freshness** — Features are materialized from offline to online on a schedule

### Registry

The registry is the metadata catalog that tracks:

- Feature definitions (names, types, entities)
- Data sources and their schemas
- Feature services (groups of features for a use case)
- Feature lineage and versioning

## Core Concepts

### Entity

An entity is a real-world object that features are associated with. Examples:
- `user_id` — Features like account age, spending patterns
- `transaction_id` — Features like amount, merchant category
- `merchant_id` — Features like fraud rate, average transaction size

Entities define the primary key for feature lookups. When requesting online features, you provide entity key-value pairs.

### Feature View

A feature view defines a group of related features from a single data source. It specifies:
- Which entity the features belong to
- The data source (e.g., a parquet file or table)
- The schema (feature names and types)
- The TTL (time-to-live) for online features

```python
user_features_view = FeatureView(
    name="user_features",
    entities=[user_entity],
    schema=[Field(name="account_age_days", dtype=Int64), ...],
    source=user_source,
    ttl=timedelta(days=1),
)
```

### Feature Service

A feature service groups multiple feature views together for a specific use case. For example, a fraud detection service might combine user features, transaction features, and aggregation features.

### Data Source

A data source connects Feast to the underlying data. Common types:
- `FileSource` — Local or S3 parquet files (great for development)
- `BigQuerySource` — Google BigQuery tables
- `RedshiftSource` — AWS Redshift tables
- `SnowflakeSource` — Snowflake tables

## Point-in-Time Correctness

This is one of the most critical concepts in feature stores.

### The Problem

When creating training data, you need features **as they were at the time of each training example**, not as they are now. Using current feature values for historical training examples causes **data leakage** — the model trains on information that wouldn't have been available at prediction time.

### How It Works

Point-in-time joins match each training example (identified by entity key + event timestamp) with the most recent feature values that were available **before** that timestamp.

```
Training example: user_id=123, event_time=2024-03-15 10:00:00

Available feature rows for user_id=123:
  2024-03-14 08:00:00 → account_age=365, avg_spend=50.0  ← This one is used
  2024-03-15 12:00:00 → account_age=366, avg_spend=55.0  ← NOT used (future)
```

### Why It Prevents Data Leakage

Without point-in-time correctness, a naive join might use the latest features, which could contain information derived from events **after** the training example occurred. For fraud detection, this would mean the model could see aggregated transaction patterns that include the fraudulent transaction itself.

## Materialization

Materialization is the process of copying feature values from the offline store to the online store. It runs on a schedule or is triggered manually.

```
Offline Store (Parquet/BigQuery) → Materialization → Online Store (Redis/DynamoDB)
```

Key considerations:
- **Frequency** — How often features are refreshed (impacts feature freshness)
- **Incremental vs Full** — Materialize only new data or recompute everything
- **Backfill** — Materializing historical data to populate the online store initially

## Feature Freshness

Feature freshness describes how up-to-date features are in the online store. Categories:

| Freshness | Latency | Example |
|---|---|---|
| Batch (hours/days) | Minutes to hours | User demographics, historical aggregates |
| Near-real-time (minutes) | Seconds to minutes | Rolling 1-hour transaction count |
| Real-time (streaming) | Milliseconds | Current session features |

Feast primarily supports batch and near-real-time freshness. For true streaming features, you'd integrate with a stream processor (e.g., Kafka + Flink).

## Feature Serving Patterns

### Online Serving (Synchronous)

Client sends entity keys → feature store returns latest feature vector → model makes prediction.

Used for: Real-time inference (fraud detection at transaction time).

### Offline Serving (Batch)

Feature store joins features to a large set of entities + timestamps → returns a training DataFrame.

Used for: Model training, batch scoring, backtesting.

### On-Demand Features

Features computed at request time from the request context (not pre-materialized). Example: time since last transaction = now - last_transaction_timestamp.

## Feature Drift Detection

Feature drift occurs when the statistical distribution of features changes over time. Monitoring for drift is crucial because:

- Input drift can degrade model performance even when the model hasn't changed
- It can indicate data pipeline issues (broken upstream data sources)
- Gradual drift may require model retraining

Common drift detection methods:
- **Population Stability Index (PSI)** — Measures distribution shift between reference and current data
- **Kolmogorov-Smirnov test** — Non-parametric test comparing two distributions
- **Jensen-Shannon divergence** — Symmetric measure of distribution similarity

## Feast Architecture Internals

Feast components:
1. **Feature Repository** — Python files defining entities, views, services
2. **Registry** — SQLite/S3/GCS file tracking metadata
3. **Online Store** — Redis, DynamoDB, or SQLite for low-latency lookups
4. **Offline Store** — File-based, BigQuery, Redshift for historical data
5. **Provider** — Abstraction layer for infrastructure (local, GCP, AWS)

The `feast apply` command parses feature definitions and updates the registry. `feast materialize` copies data from offline to online store.

## Comparison with Other Feature Stores

| Feature | Feast | Tecton | Hopsworks | Vertex AI FS |
|---|---|---|---|---|
| Open source | Yes | No (managed) | Yes (+ managed) | No (GCP managed) |
| Real-time features | Limited | Yes (streaming) | Yes (streaming) | Yes |
| Feature monitoring | Basic | Built-in | Built-in | Built-in |
| Transformations | Python (offline) | Python/SQL | Python/SQL | SQL |
| Deployment | Self-hosted | SaaS | Self-hosted/SaaS | GCP |

## Best Practices

1. **Name features descriptively** — `user_avg_transaction_amount_7d` over `feat_1`
2. **Set appropriate TTLs** — Stale features can be worse than no features
3. **Version feature views** — Track schema changes to avoid breaking downstream models
4. **Monitor feature freshness** — Alert when materialization falls behind
5. **Use point-in-time joins for training** — Never join on latest values
6. **Keep feature computation idempotent** — Re-running should produce the same results
7. **Document feature semantics** — What does the feature represent? How is it computed?

## Common Pitfalls

1. **Training-serving skew** — Different code paths for training vs inference features
2. **Data leakage via incorrect joins** — Using future data in training features
3. **Stale online features** — Materialization lag causing outdated predictions
4. **Feature explosion** — Creating too many features without pruning unused ones
5. **Missing entity keys** — Online store returns null when entity hasn't been materialized
6. **Time zone issues** — Inconsistent timestamp handling between sources

## Key Terminology

- **Entity** — Real-world object that features describe (user, transaction)
- **Feature View** — Group of related features from a single source
- **Feature Service** — Collection of feature views for a use case
- **Materialization** — Copying features from offline to online store
- **Point-in-time join** — Temporal join that prevents data leakage
- **TTL (Time-to-Live)** — Maximum age of a feature before it's considered stale
- **Training-serving skew** — Difference between features at training vs serving time
- **Feature freshness** — How recently the online store was updated
- **Feature drift** — Change in feature distribution over time
- **Registry** — Metadata catalog of feature definitions
