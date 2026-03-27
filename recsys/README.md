# Hybrid Recommendation Engine

A recommendation system combining collaborative filtering (matrix factorization), content-based filtering, and a neural hybrid approach with proper evaluation, cold-start handling, and a serving API.

## Learning Objectives

- Understand the landscape of recommendation systems and their trade-offs
- Implement collaborative filtering using ALS matrix factorization and SVD
- Build content-based filtering with TF-IDF item feature representations
- Design a neural collaborative filtering model with learned embeddings
- Combine multiple signals into a hybrid recommender
- Evaluate recommendations with ranking metrics (NDCG, MRR, Precision@K)
- Handle cold-start scenarios with popularity and content-based fallbacks
- Serve recommendations through a two-stage candidate generation + ranking pipeline
- Build a FastAPI endpoint for real-time recommendation serving

## Project Description

This project walks through building a production-style recommendation engine from the ground up. You will generate synthetic user-item interaction data, implement three distinct recommendation approaches, combine them into a hybrid model, and serve predictions through an API.

The focus is on understanding the fundamental algorithms, evaluation pitfalls (e.g., popularity bias, position bias), and architectural patterns (two-stage retrieval) used in real-world recommendation systems.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  Serving Layer                   │
│            FastAPI /recommend/{user_id}          │
├─────────────────────────────────────────────────┤
│              Two-Stage Pipeline                  │
│  ┌──────────────────┐  ┌──────────────────────┐ │
│  │    Candidate      │  │      Ranking         │ │
│  │    Generation     │──│      Model           │ │
│  │  (fast retrieval) │  │  (precise scoring)   │ │
│  └──────────────────┘  └──────────────────────┘ │
├─────────────────────────────────────────────────┤
│                  Model Layer                     │
│  ┌────────────┐ ┌───────────┐ ┌──────────────┐ │
│  │Collaborative│ │ Content-  │ │   Neural     │ │
│  │ Filtering   │ │  Based    │ │   Collab.    │ │
│  │ (ALS/SVD)   │ │ (TF-IDF)  │ │  Filtering   │ │
│  └──────┬─────┘ └─────┬─────┘ └──────┬───────┘ │
│         └──────────────┼──────────────┘         │
│                   Hybrid Model                   │
├─────────────────────────────────────────────────┤
│               Cold-Start Handling                │
│  ┌──────────────────┐  ┌──────────────────────┐ │
│  │   Popularity     │  │   Content Fallback   │ │
│  │   Baseline       │  │   (new items/users)  │ │
│  └──────────────────┘  └──────────────────────┘ │
├─────────────────────────────────────────────────┤
│                  Data Layer                      │
│  Dataset loading · Preprocessing · Splitting     │
│  Synthetic data generation · Sparse matrices     │
└─────────────────────────────────────────────────┘
```

## Implementation Tasks

### Phase 1: Data Foundation
1. Implement synthetic data generation (users, items, interactions)
2. Build user/item ID mapping and sparse interaction matrix construction
3. Implement temporal train/test splitting

### Phase 2: Core Models
4. Implement ALS matrix factorization
5. Implement truncated SVD collaborative filtering
6. Build TF-IDF content-based filtering with item features
7. Implement Neural Collaborative Filtering with embedding layers
8. Create hybrid model combining all signals

### Phase 3: Evaluation
9. Implement ranking metrics (Precision@K, Recall@K, NDCG@K, MRR, Hit Rate)
10. Implement system-level metrics (Coverage, Diversity, Novelty)
11. Build evaluation pipeline with proper negative sampling

### Phase 4: Cold-Start & Serving
12. Implement popularity-based fallback
13. Implement content-based fallback for new items
14. Build two-stage candidate generation + ranking pipeline
15. Create FastAPI serving endpoint

## Evaluation Criteria

- All models can be trained on synthetic data and produce ranked recommendations
- Evaluation metrics are correctly computed against held-out test interactions
- Cold-start fallbacks gracefully handle unseen users and items
- The hybrid model outperforms individual models on at least one metric
- API returns valid recommendation lists with scores
- Tests pass for collaborative filtering, evaluation, hybrid model, and API

## Resources

- [Matrix Factorization Techniques for Recommender Systems (Koren et al., 2009)](https://datajobs.com/data-science-repo/Recommender-Systems-[Netflix].pdf)
- [Neural Collaborative Filtering (He et al., 2017)](https://arxiv.org/abs/1708.05031)
- [Deep Learning based Recommender System: A Survey (Zhang et al., 2019)](https://arxiv.org/abs/1707.07435)
- [Evaluating Recommendation Systems (Shani & Gunawardana)](https://link.springer.com/chapter/10.1007/978-0-387-85820-3_8)
- [Implicit Feedback for Recommender Systems (Hu et al., 2008)](http://yifanhu.net/PUB/cf.pdf)
- [Two-Tower Models for Retrieval](https://blog.reachsumit.com/posts/2023/03/two-tower-model/)
- [Surprise library documentation](https://surprise.readthedocs.io/)
- [PyTorch documentation](https://pytorch.org/docs/stable/)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
