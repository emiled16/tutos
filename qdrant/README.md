# Semantic Search & RAG Engine — Qdrant

## Overview

Build a semantic search engine using Qdrant with hybrid search (dense + sparse vectors), filtering, payload indexing, and a RAG (Retrieval-Augmented Generation) pipeline. The project covers the full lifecycle from document ingestion to answer generation with citations.

## Learning Objectives

- Set up and configure Qdrant collections with appropriate vector and index settings
- Implement document chunking strategies (fixed-size, semantic, recursive)
- Generate dense embeddings (sentence-transformers) and sparse vectors (BM25/SPLADE)
- Build hybrid search combining dense and sparse retrieval with Reciprocal Rank Fusion
- Apply metadata filters (must, should, must_not) for filtered search
- Construct a RAG pipeline: retrieve context, generate answers with citations
- Evaluate retrieval quality with standard IR metrics (precision@k, recall@k, MRR, NDCG)

## Project Description

You will build a **Semantic Search & RAG Engine** that:

1. **Ingests documents** — processes a corpus into chunks with metadata
2. **Generates embeddings** — creates dense vectors (sentence-transformers) and sparse vectors (BM25)
3. **Indexes into Qdrant** — batch-uploads vectors with payload metadata
4. **Searches** — supports dense, sparse, hybrid, and filtered search modes
5. **Generates answers** — RAG pipeline retrieves context and produces cited answers
6. **Evaluates** — measures retrieval quality with standard IR metrics

## Architecture

```
Documents
    │
    ▼
┌────────────────┐
│ Document       │ ─── Chunking (fixed / semantic / recursive)
│ Processor      │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│   Embedder     │ ─── Dense (sentence-transformers) + Sparse (BM25)
└───────┬────────┘
        │
        ▼
┌────────────────┐
│   Indexer      │ ─── Batch upload to Qdrant with payloads
└───────┬────────┘
        │
        ▼
┌────────────────────────────────────────┐
│            Qdrant Collection           │
│  ┌──────────┐  ┌────────┐  ┌───────┐  │
│  │ Dense    │  │ Sparse │  │Payload│  │
│  │ Vectors  │  │ Vectors│  │ Index │  │
│  └──────────┘  └────────┘  └───────┘  │
└───────┬────────────────────────────────┘
        │
   ┌────┼────────────┐
   ▼    ▼            ▼
Dense  Sparse    Filtered
Search Search    Search
   │    │            │
   └────┼────────────┘
        ▼
   ┌─────────┐
   │ Hybrid  │ ─── RRF Fusion
   │ Search  │
   └────┬────┘
        ▼
   ┌─────────┐
   │   RAG   │ ─── Retrieve → Generate → Cite
   │Pipeline │
   └─────────┘
```

## Implementation Tasks

### Phase 1 — Collection & Ingestion
- [ ] Create and configure Qdrant collection with dense + sparse vector spaces
- [ ] Implement document chunking strategies
- [ ] Generate dense embeddings with sentence-transformers
- [ ] Generate sparse vectors with BM25/SPLADE
- [ ] Batch-index chunks with metadata payloads

### Phase 2 — Search
- [ ] Implement dense vector similarity search
- [ ] Implement sparse (BM25) search
- [ ] Implement hybrid search with RRF fusion
- [ ] Implement filtered search with payload conditions

### Phase 3 — RAG Pipeline
- [ ] Build retriever that fetches top-k relevant chunks
- [ ] Build generator that produces answers from context
- [ ] Wire up end-to-end RAG pipeline with citation tracking

### Phase 4 — Evaluation & Polish
- [ ] Implement retrieval metrics (precision@k, recall@k, MRR, NDCG)
- [ ] Create sample data corpus for testing
- [ ] Write comprehensive tests for all components

## Evaluation Criteria

- Collection is configured with appropriate HNSW parameters and payload indices
- Chunking produces reasonable chunk sizes with meaningful overlap
- Dense and sparse embeddings are correctly generated and indexed
- Hybrid search with RRF produces better results than either modality alone
- Filtered search correctly applies must/should/must_not conditions
- RAG pipeline generates grounded answers with proper citations
- Retrieval metrics are correctly computed
- Tests cover collection management, search, and the RAG pipeline

## Resources

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Qdrant Python Client](https://github.com/qdrant/qdrant-client)
- [Sentence Transformers](https://www.sbert.net/)
- [FastEmbed](https://github.com/qdrant/fastembed)
- [Reciprocal Rank Fusion Paper](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- [RAG Survey Paper](https://arxiv.org/abs/2312.10997)
- [Chunking Strategies for RAG](https://www.pinecone.io/learn/chunking-strategies/)
