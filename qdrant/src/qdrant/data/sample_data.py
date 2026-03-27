"""Sample document corpus for testing and development."""

from __future__ import annotations

from qdrant.indexing.document_processor import Document


def get_sample_documents() -> list[Document]:
    """Generate a sample corpus of documents for testing.

    Returns a diverse set of short documents across topics
    for development and evaluation purposes.

    Returns:
        List of sample Document instances.
    """
    # TODO: Implement sample data generation
    # Create 20-30 Document instances across topics like:
    # - Machine learning basics
    # - Python programming
    # - Data engineering
    # - Cloud computing
    # Each document should be 200-500 words with realistic content
    # and metadata (source, category, date, author)
    pass


def get_evaluation_queries() -> list[dict]:
    """Get a set of queries with ground-truth relevant document IDs.

    Returns:
        List of {"query": str, "relevant_ids": set[str]} dicts
        for evaluation.
    """
    # TODO: Implement evaluation query set
    # Create 10-15 queries with known relevant documents
    # from the sample corpus above
    pass
