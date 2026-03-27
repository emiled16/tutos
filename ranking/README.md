# Search Ranking System

Build a learning-to-rank system for search results using gradient boosted trees (LambdaMART).

## Learning Objectives

- Understand information retrieval fundamentals and BM25 scoring
- Implement feature engineering for query-document pairs
- Train pointwise, pairwise, and listwise ranking models
- Evaluate ranking quality with standard IR metrics (NDCG, MRR, MAP)
- Serve real-time rankings through a FastAPI endpoint
- Understand the LambdaMART algorithm and lambda gradients

## Project Description

This project implements a two-stage ranking system: a retrieval stage that generates candidate documents and a re-ranking stage that uses machine-learned features to produce the final ordering. You will build feature extractors for query-level, document-level, and query-document interaction signals, then train models using three learning-to-rank paradigms before exposing the ranker as an HTTP service.

## Architecture

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────┐
│  Query   │────▸│  Feature     │────▸│  Ranking     │────▸│  Ranked  │
│  Input   │     │  Pipeline    │     │  Model       │     │  Results │
└──────────┘     └──────────────┘     └──────────────┘     └──────────┘
                   │  │  │                │  │  │
            ┌──────┘  │  └──────┐   ┌────┘  │  └────┐
            ▼         ▼        ▼   ▼       ▼       ▼
         Query    Document  Inter- Point- Pair-  Lambda-
         Feats    Feats     action wise   wise   MART
```

### Module Layout

```
src/ranking/
├── features/          # Feature engineering
│   ├── query_features.py
│   ├── document_features.py
│   ├── interaction_features.py
│   └── feature_pipeline.py
├── models/            # Ranking models
│   ├── pointwise.py
│   ├── pairwise.py
│   └── lambdamart.py
├── evaluation/        # IR metrics and evaluation
│   ├── metrics.py
│   └── evaluator.py
├── data/              # Dataset loading and generation
│   ├── data_loader.py
│   └── data_generator.py
└── serving/           # API and online ranking
    ├── api.py
    └── ranker.py
```

## Implementation Tasks

1. **Feature Engineering** — Implement query, document, and interaction feature extractors
2. **Data Pipeline** — Load MSLR-WEB format datasets or generate synthetic ranking data
3. **Pointwise Model** — Train a regression model that predicts relevance scores independently
4. **Pairwise Model** — Implement RankNet-style pairwise learning with preference pairs
5. **LambdaMART** — Train a LightGBM LambdaMART model with NDCG-aware lambda gradients
6. **Evaluation** — Compute NDCG@k, MRR, MAP, Precision@k, and Recall@k across queries
7. **Serving** — Expose the trained ranker via a FastAPI endpoint with feature computation

## Evaluation Criteria

- Correct implementation of BM25 and TF-IDF scoring
- Feature pipeline produces consistent, reproducible feature vectors
- Models train without errors and produce meaningful score orderings
- NDCG@10 on synthetic data exceeds random baseline
- Evaluation metrics match reference implementations on known inputs
- API returns ranked results with latency under 100ms for typical queries
- Test coverage for features, metrics, models, and API endpoints

## Resources

- [Learning to Rank for Information Retrieval (Liu, 2011)](https://link.springer.com/book/10.1007/978-3-642-14267-3)
- [From RankNet to LambdaRank to LambdaMART (Burges, 2010)](https://www.microsoft.com/en-us/research/publication/from-ranknet-to-lambdarank-to-lambdamart-an-overview/)
- [LightGBM LambdaRank Documentation](https://lightgbm.readthedocs.io/en/latest/Advanced-Topics.html)
- [MSLR-WEB10K Dataset](https://www.microsoft.com/en-us/research/project/mslr/)
- [Introduction to Information Retrieval (Manning et al.)](https://nlp.stanford.edu/IR-book/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
