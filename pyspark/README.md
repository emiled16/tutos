# Large-Scale Feature Factory — PySpark

## Overview

Build a PySpark feature engineering pipeline that processes a large e-commerce dataset. Implement window functions, UDFs, proper partitioning strategies, broadcast joins, caching, and Delta Lake integration for feature versioning.

## Learning Objectives

- Configure and tune a SparkSession for local development and cluster execution
- Implement feature engineering at scale using PySpark transformations
- Master window functions for time-series and ranking features
- Apply proper partitioning and caching strategies for performance
- Integrate Delta Lake for ACID-compliant feature storage with time travel
- Write testable PySpark code using the chispa testing library
- Identify and fix common performance anti-patterns

## Project Description

You will build a **Feature Factory** that ingests synthetic e-commerce data (users, products, transactions, clickstream) and produces feature tables ready for machine learning. The pipeline demonstrates real-world PySpark patterns:

1. **Data ingestion** — read from CSV/Parquet/Delta with schema enforcement
2. **Cleaning** — deduplication, null handling, type casting, outlier detection
3. **User features** — lifetime value, purchase frequency, recency, session counts
4. **Product features** — popularity scores, price statistics, category embeddings
5. **Interaction features** — click-through rates, dwell times, conversion rates
6. **Window features** — rolling averages, lag features, rank within category
7. **Encoding** — one-hot, label, and target encoding
8. **Output** — write feature tables to Delta Lake with proper partitioning

## Architecture

```
Raw Data (CSV/Parquet)
        │
        ▼
  ┌──────────┐
  │ Readers  │ ─── Schema enforcement, type casting
  └────┬─────┘
       ▼
  ┌──────────┐
  │ Cleaning │ ─── Dedup, nulls, outliers
  └────┬─────┘
       ▼
  ┌──────────────────────────────────┐
  │       Feature Engineering        │
  │  ┌──────┐ ┌───────┐ ┌────────┐  │
  │  │ User │ │Product│ │ Inter. │  │
  │  └──┬───┘ └───┬───┘ └───┬────┘  │
  │     └─────┬───┘─────────┘       │
  │           ▼                      │
  │    ┌────────────┐                │
  │    │  Window    │                │
  │    │  Features  │                │
  │    └────────────┘                │
  └──────────┬───────────────────────┘
             ▼
  ┌──────────────┐
  │   Encoding   │
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │  Writers     │ ─── Delta Lake with partitioning
  └──────────────┘
```

## Implementation Tasks

### Phase 1 — Setup & Data Generation
- [ ] Configure SparkSession with Delta Lake support (`app.py`)
- [ ] Generate synthetic e-commerce data (`data_generator.py`)
- [ ] Implement data readers with schema enforcement (`io/readers.py`)

### Phase 2 — Data Cleaning
- [ ] Implement deduplication logic
- [ ] Handle null values (fill, drop, flag strategies)
- [ ] Cast types and normalize formats

### Phase 3 — Feature Engineering
- [ ] User features: lifetime value, purchase frequency, recency
- [ ] Product features: popularity, price stats, category aggregates
- [ ] Interaction features: CTR, dwell time, conversion rate
- [ ] Window features: rolling averages, lag, rank

### Phase 4 — Encoding & Output
- [ ] One-hot, label, and target encoding transforms
- [ ] Complex aggregations with groupBy and window specs
- [ ] Write to Delta Lake with partitioning
- [ ] Spark tuning helpers (shuffle partitions, memory, broadcast threshold)

### Phase 5 — Testing
- [ ] Write tests using chispa for DataFrame equality
- [ ] Test individual feature functions
- [ ] Test full pipeline end-to-end

## Evaluation Criteria

- SparkSession is properly configured for local and cluster modes
- Feature functions are pure transformations (DataFrame in, DataFrame out)
- Window functions use correct partitioning and ordering
- Broadcast joins are used where appropriate (small dimension tables)
- Caching is applied strategically (not over- or under-cached)
- Delta Lake writes use proper partitioning columns
- Tests use chispa for readable DataFrame assertions
- No `collect()` on large DataFrames; no Python UDFs where Spark-native functions suffice

## Resources

- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Delta Lake Documentation](https://docs.delta.io/latest/)
- [chispa Testing Library](https://github.com/MrPowers/chispa)
- [Spark Performance Tuning Guide](https://spark.apache.org/docs/latest/sql-performance-tuning.html)
- [Window Functions in PySpark](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/window.html)
