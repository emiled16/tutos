# Hybrid Recommendation Engine — Theory Notes

## Recommendation System Landscape

Recommendation systems fall into three broad families:

- **Collaborative filtering (CF):** Leverages user-item interaction patterns. "Users who liked X also liked Y." No item content needed, but suffers from cold-start.
- **Content-based filtering (CBF):** Uses item (and optionally user) features to recommend similar items. Works for new items if features are available but can over-specialize.
- **Hybrid approaches:** Combine CF and CBF signals to get the best of both worlds — CF captures latent taste patterns while CBF covers cold-start gaps.

Modern production systems (YouTube, Netflix, Spotify) use deep learning hybrids with a two-stage architecture: fast candidate generation followed by precise ranking.

## Collaborative Filtering

### User-Based CF

Find users similar to the target user (via cosine similarity, Pearson correlation on rating vectors), then recommend items those similar users liked. Simple but does not scale — computing pairwise user similarities is O(n²) and the user-item matrix is extremely sparse.

### Item-Based CF

Compute item-item similarities from the co-occurrence patterns in user interactions. More stable than user-based CF because item profiles change less frequently than user profiles. Amazon popularized this approach.

### Matrix Factorization

Decompose the sparse user-item interaction matrix R (m users × n items) into two low-rank matrices:

```
R ≈ U · V^T
```

where U ∈ ℝ^(m×k) and V ∈ ℝ^(n×k). Each user and item gets a k-dimensional latent factor vector. The predicted rating for user u and item i is:

```
r̂(u,i) = u_u · v_i^T + b_u + b_i + μ
```

where b_u, b_i are user/item biases and μ is the global mean.

## Content-Based Filtering

Represent each item as a feature vector (genres, tags, text descriptions). Common approaches:

- **TF-IDF** on text features (titles, descriptions, tags) — simple, interpretable, effective
- **Pretrained embeddings** (BERT, sentence-transformers) for richer semantic representations
- **One-hot / multi-hot encoding** for categorical features (genre, category)

Given a user profile (aggregated from their liked items' feature vectors), recommend items whose feature vectors are most similar (cosine similarity).

Strengths: handles new items immediately, provides explainable recommendations ("because you liked items with feature X"). Weakness: limited to recommending items similar to what users have already seen (filter bubble).

## Hybrid Approaches

Strategies for combining CF and CBF:

- **Weighted hybrid:** Score = α · CF_score + (1-α) · CBF_score. Simple but α is hard to tune.
- **Switching hybrid:** Use CBF for cold-start users/items, CF for warm users.
- **Feature augmentation:** Use CBF features as additional input to the CF model.
- **Meta-level:** Train one model on the output of another.
- **Neural hybrid:** Feed user/item embeddings AND content features into a neural network that learns the optimal combination.

## Implicit vs Explicit Feedback

**Explicit feedback** (ratings 1-5) directly expresses preference but is scarce — most users don't rate items.

**Implicit feedback** (clicks, views, purchases, time spent) is abundant but noisy:
- Presence signals interest, absence is ambiguous (user didn't see it vs. saw it and wasn't interested)
- No negative signals — requires careful negative sampling
- Frequency/duration can proxy for preference strength

Most real-world systems rely on implicit feedback. The loss function changes: instead of minimizing rating prediction error (MSE), optimize ranking quality (BPR loss, weighted matrix factorization).

## ALS (Alternating Least Squares)

ALS solves the matrix factorization objective by alternating between:

1. Fix V, solve for U: each user vector u_u is a ridge regression problem
2. Fix U, solve for V: each item vector v_i is a ridge regression problem

Each sub-problem has a closed-form solution:

```
u_u = (V^T · C_u · V + λI)^(-1) · V^T · C_u · p_u
```

where C_u is a diagonal confidence matrix and p_u is the binary preference vector (for implicit feedback, following Hu et al. 2008).

ALS advantages: naturally parallelizable (rows are independent), handles implicit feedback well, scales to large datasets. Disadvantage: memory-intensive for very large factor matrices.

## SVD for Recommendations

Truncated SVD decomposes the (mean-centered) interaction matrix:

```
R ≈ U_k · Σ_k · V_k^T
```

keeping only the top-k singular values. This gives the best rank-k approximation in Frobenius norm.

Practical notes:
- Must handle missing values carefully — can't apply SVD directly to a sparse matrix with zeros as "missing"
- Often use iterative imputation or only decompose observed entries
- scikit-learn's `TruncatedSVD` works on sparse matrices efficiently
- Funk SVD (SGD-based) optimizes only on observed entries, avoiding the imputation problem

## Neural Collaborative Filtering (NCF)

Replace the dot product in matrix factorization with a neural network:

```
Input: (user_id, item_id)
  → user_embedding, item_embedding (learned lookup tables)
  → concatenate [user_emb; item_emb]
  → MLP layers with ReLU
  → output score (sigmoid for implicit, linear for explicit)
```

The original NCF paper (He et al. 2017) proposes GMF + MLP fusion:
- **GMF (Generalized Matrix Factorization):** Element-wise product of user and item embeddings
- **MLP:** Concatenated embeddings through dense layers
- **NeuMF:** Concatenate GMF and MLP outputs, final prediction layer

Advantages: learns non-linear user-item interactions, flexible architecture. Disadvantages: needs more data, training is slower than ALS/SVD, harder to interpret.

## Embedding Tables

Each user and item is assigned a learnable embedding vector via `nn.Embedding(num_entities, embedding_dim)`. This is a lookup table — for user_id=42, return the 42nd row of the embedding matrix.

Key design decisions:
- **Embedding dimension:** Typically 32-256. Larger = more expressive but more parameters
- **Initialization:** Xavier/He uniform, or pretrained (e.g., from SVD factors)
- **Regularization:** Weight decay, dropout on embeddings, or embedding dropout (zero out entire embedding vectors)

## Negative Sampling Strategies

For implicit feedback, we need to construct negative examples (items the user presumably isn't interested in):

- **Uniform random:** Sample random unobserved items. Simple but may sample popular items the user would actually like.
- **Popularity-based:** Sample negatives proportional to item popularity. Harder negatives improve learning.
- **In-batch negatives:** Use other users' positive items as negatives. Efficient but introduces popularity bias.
- **Hard negative mining:** Use the model's own predictions to find informative negatives (items the model incorrectly ranks highly).

Negative-to-positive ratio matters — typically 4:1 to 10:1 works well. Too many negatives slow training; too few cause the model to overfit.

## Evaluation Challenges

### Offline vs Online Evaluation

**Offline evaluation** uses historical data with a held-out test set. Fast and cheap, but has fundamental limitations:
- Can only evaluate items users actually interacted with — a recommended item might be excellent but gets scored as a "miss" if the user never saw it
- Doesn't capture novelty, serendipity, or long-term user engagement

**Online evaluation** (A/B testing) measures real user behavior (CTR, engagement time, conversions). Ground truth but expensive, slow, and risky (bad recommendations hurt users).

**Counterfactual evaluation** (IPS, doubly-robust estimators) attempts to correct for selection bias in logged data.

### Temporal Splitting

Always split by time, not randomly. Random splitting causes data leakage — the model trains on future interactions to predict past ones. Use the last N interactions per user, or a global timestamp cutoff.

## Cold-Start Problem and Solutions

**User cold-start:** New user with no interaction history.
- Popularity-based recommendations (most popular items)
- Ask for explicit preferences (onboarding quiz)
- Use demographic features if available
- Bandits (explore to learn preferences quickly)

**Item cold-start:** New item with no interactions.
- Content-based recommendation using item features
- Promote new items with exploration bonuses
- Use side information (item metadata, description embeddings)

**System cold-start:** New system with no data at all.
- Content-based only until sufficient interactions accumulate
- Transfer learning from similar domains

## Two-Stage Architecture

Production systems split recommendation into two stages:

### Stage 1: Candidate Generation
- Retrieve a manageable set (100-1000) from millions of items
- Must be fast — approximate nearest neighbor search (FAISS, Annoy, ScaNN)
- Models: two-tower (separate user/item encoders), item-CF, popularity
- Multiple candidate generators run in parallel and their results are merged

### Stage 2: Ranking
- Score and re-rank the candidate set with a more expressive model
- Can afford to be slow — only scoring hundreds of items
- Feature-rich model: user features, item features, context, cross-features
- Often a deep neural network or gradient-boosted trees

## Exploration vs Exploitation

**Exploitation:** Recommend items the system is confident the user will like. Maximizes short-term engagement but narrows the user's experience.

**Exploration:** Recommend uncertain items to gather information. Short-term cost for long-term gain — discovers new user interests, surfaces tail content.

Approaches:
- **ε-greedy:** With probability ε, recommend a random item instead of the top prediction
- **Thompson Sampling:** Sample from the posterior distribution of item quality
- **Upper Confidence Bound (UCB):** Recommend items with high uncertainty-adjusted scores
- **Entropy regularization:** Add a diversity term to the recommendation objective

## Diversity-Accuracy Tradeoff

Optimizing purely for accuracy (predicted relevance) produces homogeneous recommendations — a user who likes action movies gets only action movies. This hurts user satisfaction and content discovery.

Metrics capturing diversity:
- **Intra-list diversity:** Average pairwise distance between recommended items
- **Coverage:** Fraction of the item catalog that appears in any user's recommendations
- **Novelty:** How surprising the recommendations are (inverse popularity)

Re-ranking for diversity:
- **MMR (Maximal Marginal Relevance):** Iteratively select items that are both relevant and different from already-selected items
- **DPP (Determinantal Point Processes):** Sample diverse subsets with probability proportional to the determinant of a similarity kernel

## Popularity Bias

Popular items dominate recommendations because:
- They have more interactions → better-estimated latent factors
- Evaluation metrics favor them (users interact with popular items more, so they appear in test sets)
- Feedback loops: recommended → more interactions → recommended more

Mitigation:
- Inverse propensity scoring in evaluation
- Calibrated recommendations (match the user's genre distribution)
- Popularity-stratified evaluation (report metrics separately for popular/niche items)

## Position Bias in Recommendations

Users interact more with items shown in higher positions, regardless of item quality. This creates a feedback loop:

1. Item placed at position 1 gets clicked
2. System interprets click as positive signal
3. Item is recommended at position 1 again

Correcting for position bias:
- **Position-aware models:** Include position as a feature during training, set to a default at inference
- **Inverse propensity weighting:** Weight each interaction by 1/P(click|position)
- **Randomized experiments:** Occasionally shuffle positions to get unbiased signals
- **Click models:** Separate examination probability (position-dependent) from relevance probability
