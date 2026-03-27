# Search Ranking — Theory Notes

## Information Retrieval Fundamentals

Information retrieval (IR) is the task of finding documents from a large collection that satisfy a user's information need, expressed as a query. The core challenge is estimating **relevance**: how well a document satisfies the query intent.

Classic IR uses an inverted index to map terms to documents. At query time, candidate documents are retrieved and scored. Modern search systems extend this with machine-learned ranking.

### Key Concepts

- **Precision**: Fraction of retrieved documents that are relevant
- **Recall**: Fraction of relevant documents that are retrieved
- **The precision-recall tradeoff**: Retrieving more documents increases recall but typically decreases precision

## BM25 Scoring

BM25 (Best Matching 25) is a probabilistic retrieval function that scores query-document relevance:

$$\text{BM25}(q, d) = \sum_{t \in q} \text{IDF}(t) \cdot \frac{f(t, d) \cdot (k_1 + 1)}{f(t, d) + k_1 \cdot \left(1 - b + b \cdot \frac{|d|}{\text{avgdl}}\right)}$$

Where:
- $f(t, d)$ is the term frequency of $t$ in document $d$
- $|d|$ is the document length, $\text{avgdl}$ is average document length
- $k_1$ (typically 1.2–2.0) controls term frequency saturation
- $b$ (typically 0.75) controls length normalization
- $\text{IDF}(t) = \log \frac{N - n(t) + 0.5}{n(t) + 0.5}$ where $N$ is total documents, $n(t)$ is documents containing $t$

BM25 improves on raw TF-IDF by saturating term frequency (diminishing returns for repeated terms) and normalizing for document length.

## Learning-to-Rank Approaches

Learning-to-rank (LTR) applies machine learning to the ranking problem. Three paradigms exist, distinguished by their loss functions.

### Pointwise

Treats ranking as regression or classification on individual documents. Each query-document pair gets a relevance score prediction.

- **Loss**: MSE between predicted and true relevance labels
- **Pros**: Simple to implement, uses standard ML models
- **Cons**: Ignores relative ordering between documents; optimizes per-document accuracy, not list quality

### Pairwise

Learns from pairs of documents for the same query, predicting which document should rank higher.

- **Loss**: Cross-entropy on pairwise preferences (RankNet uses $\sigma(s_i - s_j)$ as the predicted probability that $d_i \succ d_j$)
- **Pros**: Directly optimizes relative ordering
- **Cons**: Number of pairs is $O(n^2)$ per query; all pairs weighted equally regardless of position

### Listwise

Optimizes the entire ranked list directly, typically targeting an IR metric like NDCG.

- **Loss**: Defined over permutations or metric surrogates
- **Pros**: Directly optimizes the evaluation metric; position-aware
- **Cons**: More complex to implement; metrics like NDCG are non-differentiable and require approximation

## LambdaMART Algorithm

LambdaMART combines **LambdaRank** (lambda gradients for pairwise learning) with **MART** (Multiple Additive Regression Trees, i.e., gradient boosted trees).

### Lambda Gradients

The key insight: instead of defining an explicit loss function, define the gradients directly. For a pair $(i, j)$ where $d_i$ should rank above $d_j$:

$$\lambda_{ij} = \frac{-\sigma}{1 + e^{\sigma(s_i - s_j)}} \cdot |\Delta \text{NDCG}_{ij}|$$

Where $|\Delta \text{NDCG}_{ij}|$ is the change in NDCG from swapping documents $i$ and $j$. This weighting means:
- Pairs near the top of the ranking get larger gradients (position-aware)
- Pairs whose swap would change NDCG more get larger gradients (metric-aware)
- The sigmoid term means mis-ordered pairs get stronger corrections

### Training Procedure

1. Initialize scores to zero
2. For each boosting round:
   a. Compute lambda gradients for all pairs in each query
   b. Fit a regression tree to the lambdas
   c. Update leaf values using Newton's method (using the Hessians)
   d. Add the tree to the ensemble with a learning rate

## NDCG and Its Properties

Normalized Discounted Cumulative Gain (NDCG) measures ranking quality with position-dependent discounting:

$$\text{DCG}@k = \sum_{i=1}^{k} \frac{2^{r_i} - 1}{\log_2(i + 1)}$$

$$\text{NDCG}@k = \frac{\text{DCG}@k}{\text{IDCG}@k}$$

Where $\text{IDCG}@k$ is the DCG of the ideal (perfectly sorted) ranking.

### Properties

- **Bounded**: NDCG ∈ [0, 1], with 1 being perfect ranking
- **Position-discounted**: Top positions matter exponentially more than lower ones
- **Graded relevance**: Unlike MAP, handles multiple relevance levels (not just binary)
- **Query-normalized**: Comparable across queries with different numbers of relevant documents
- **Not metric-continuous**: Small score changes can cause large NDCG jumps (rank swaps at the top)

## Position Bias in Clicks

Users are more likely to click results at higher positions regardless of relevance. This creates a feedback loop: highly-ranked items get more clicks, which can reinforce their position.

### Click Models

- **Position model**: $P(\text{click}) = P(\text{examine}) \cdot P(\text{relevant})$ where $P(\text{examine})$ decreases with position
- **Cascade model**: User examines results top-to-bottom, stopping after finding a satisfying result
- **Inverse propensity weighting (IPW)**: De-bias click data by weighting clicks inversely by their position's examination probability

### Implications for Training

- Naively training on click data amplifies position bias
- Randomization experiments (showing slightly randomized results) can estimate position bias
- Interleaving provides unbiased comparison between rankers without full randomization

## Feature Engineering for Ranking

Ranking features fall into three categories:

### Query Features (query-dependent, document-independent)
- Query length (number of terms)
- Query term IDF statistics
- Query intent classification (navigational, informational, transactional)
- Historical query frequency

### Document Features (document-dependent, query-independent)
- PageRank or authority score
- Document length
- Freshness (age of content)
- Spam score
- URL depth
- Number of inlinks/outlinks

### Query-Document Interaction Features
- BM25 score (across different fields: title, body, anchor)
- TF-IDF cosine similarity
- Exact match signals (query appears in title, URL)
- Query term coverage (fraction of query terms found in document)
- Proximity of query terms in document

A typical production ranker uses 100–1000+ features.

## Online vs Offline Evaluation

### Offline Evaluation
Uses held-out labeled datasets with human relevance judgments.
- **Metrics**: NDCG, MAP, MRR, Precision@k
- **Pros**: Reproducible, cheap, fast iteration
- **Cons**: Labels are expensive; doesn't capture user satisfaction; static queries may not represent live traffic

### Online Evaluation
Measures real user behavior with live traffic.
- **Metrics**: Click-through rate, session success rate, time to first click, abandonment rate
- **Pros**: Directly measures user satisfaction; captures temporal effects
- **Cons**: Slow (needs statistical significance), risky (bad ranker hurts users), confounded by position bias

### Best Practice

Use offline evaluation for development-cycle iteration, then validate promising candidates with online A/B tests or interleaving experiments.

## Interleaving Experiments

Interleaving is more statistically efficient than A/B testing for comparing rankers. Instead of splitting users, show each user a merged result list from both rankers.

### Team Draft Interleaving
1. Two rankers each produce a ranked list
2. Alternately pick the next-best result from each ranker (like team captains drafting players)
3. Track which ranker "owns" each clicked result
4. The ranker whose results get more clicks wins

Interleaving requires ~100× fewer queries than A/B testing to reach the same statistical confidence because each user serves as their own control.

## Cascade Model of User Behavior

The cascade model assumes users examine results sequentially from top to bottom:

1. User examines result at position 1
2. If satisfied (clicks and finds relevant), user stops
3. Otherwise, user moves to position 2, and so on
4. At each position, user decides to click with probability based on relevance

This model explains why:
- Top positions have highest click rates
- Click probability drops roughly logarithmically with position
- Users rarely examine results beyond position 10
- MRR (Mean Reciprocal Rank) is a natural metric under this model

## Diversity in Ranking Results

Returning redundant results wastes ranking slots. Diversity-aware ranking accounts for:

### Subtopic Coverage
If a query is ambiguous ("jaguar" — car? animal? guitar?), cover different intents. Maximal Marginal Relevance (MMR) trades off relevance against redundancy:

$$\text{MMR} = \arg\max_{d \in R \setminus S} \left[\lambda \cdot \text{sim}(d, q) - (1-\lambda) \cdot \max_{d' \in S} \text{sim}(d, d')\right]$$

### Result Type Diversity
Mix different content types (articles, videos, images) when appropriate.

### Source Diversity
Avoid showing too many results from the same domain.

## Two-Stage Ranking Architecture

Production search systems use multiple stages for efficiency:

### Stage 1: Retrieval (Candidate Generation)
- **Goal**: High recall from millions/billions of documents
- **Methods**: Inverted index (BM25), approximate nearest neighbors, learned sparse retrieval
- **Latency budget**: ~10ms
- **Output**: ~1000 candidate documents

### Stage 2: Re-ranking
- **Goal**: High precision among candidates
- **Methods**: Machine-learned ranker with expensive features (LambdaMART, neural models)
- **Latency budget**: ~50ms
- **Output**: Final ranked list (~10-20 results)

### Why Two Stages?
Computing expensive features (cross-encoder similarity, real-time user features) for every document in the collection is infeasible. Retrieval acts as a cheap filter, and re-ranking applies the full feature set to a manageable candidate set.

Some systems add a third stage (L0 → L1 → L2) where L0 is retrieval, L1 is a lightweight re-ranker, and L2 is the full-featured model applied to the top ~100 candidates.
