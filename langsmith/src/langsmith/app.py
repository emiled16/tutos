"""Main application entry point for the LLM Evaluation Pipeline.

Provides a CLI and programmatic interface for running Q&A and summarization
against documents, with LangSmith tracing enabled.
"""

from langchain_openai import ChatOpenAI

from langsmith.chains.qa_chain import build_qa_chain
from langsmith.chains.summarization_chain import build_summarization_chain
from langsmith.prompts.prompt_registry import PromptRegistry
from langsmith.tracing.callbacks import create_tracing_callbacks
from langsmith.tracing.metadata import build_run_metadata


def create_llm(model: str = "gpt-4o-mini", temperature: float = 0.0) -> ChatOpenAI:
    """Create a configured ChatOpenAI instance.

    Args:
        model: The OpenAI model identifier.
        temperature: Sampling temperature (0.0 = deterministic).

    Returns:
        A configured ChatOpenAI instance.
    """
    # TODO: Implement — instantiate ChatOpenAI with the given parameters
    raise NotImplementedError


def answer_question(
    question: str,
    documents: list[str],
    *,
    prompt_version: str = "concise",
    model: str = "gpt-4o-mini",
    tags: list[str] | None = None,
) -> dict[str, str]:
    """Answer a question using retrieval-augmented generation.

    Constructs a Q&A chain with the specified prompt version, runs it against
    the provided documents, and returns the answer with tracing metadata.

    Args:
        question: The user's question.
        documents: List of document texts to use as context.
        prompt_version: Which prompt template to use from the registry.
        model: The OpenAI model identifier.
        tags: Optional tags for the LangSmith trace.

    Returns:
        A dict with keys "answer", "source_documents", and "run_id".
    """
    # TODO: Implement
    # 1. Create the LLM
    # 2. Load the prompt template from the registry
    # 3. Build the QA chain
    # 4. Set up tracing callbacks with metadata and tags
    # 5. Invoke the chain and return structured result
    raise NotImplementedError


def summarize_document(
    document: str,
    *,
    model: str = "gpt-4o-mini",
    tags: list[str] | None = None,
) -> dict[str, str]:
    """Summarize a document using the summarization chain.

    Args:
        document: The full document text.
        model: The OpenAI model identifier.
        tags: Optional tags for the LangSmith trace.

    Returns:
        A dict with keys "summary" and "run_id".
    """
    # TODO: Implement
    # 1. Create the LLM
    # 2. Build the summarization chain
    # 3. Set up tracing callbacks
    # 4. Invoke and return the result
    raise NotImplementedError


def compare_prompt_versions(
    question: str,
    documents: list[str],
    versions: list[str] | None = None,
) -> dict[str, dict[str, str]]:
    """Run the same question against multiple prompt versions for comparison.

    Args:
        question: The user's question.
        documents: List of document texts.
        versions: Prompt versions to compare. Defaults to all registered versions.

    Returns:
        A dict mapping version name to its answer result.
    """
    # TODO: Implement
    # 1. Get versions from registry if not specified
    # 2. Run answer_question for each version
    # 3. Collect and return results keyed by version name
    raise NotImplementedError
