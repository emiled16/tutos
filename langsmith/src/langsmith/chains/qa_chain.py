"""Retrieval-augmented Q&A chain using LangChain.

Builds an LCEL chain that takes a question and a set of documents,
retrieves the most relevant context, and generates an answer.
"""

from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough


def format_documents(documents: list[str]) -> str:
    """Join a list of document strings into a single context block.

    Args:
        documents: List of document text chunks.

    Returns:
        A single string with documents separated by double newlines.
    """
    # TODO: Implement — join documents with separator and numbering
    raise NotImplementedError


def build_qa_chain(
    llm: BaseChatModel,
    prompt: ChatPromptTemplate,
) -> Runnable:
    """Build an LCEL chain for question answering with document context.

    The chain expects a dict input with keys "question" and "documents".
    It formats the documents into a context string, passes them through
    the prompt template, and generates an answer.

    Args:
        llm: The language model to use for generation.
        prompt: The prompt template with placeholders for "context" and "question".

    Returns:
        An LCEL Runnable that accepts {"question": str, "documents": list[str]}
        and returns a string answer.
    """
    # TODO: Implement
    # 1. Create a preprocessing step that formats documents into context
    # 2. Chain: preprocess -> prompt -> llm -> output_parser
    # Use RunnablePassthrough.assign() to inject formatted context
    raise NotImplementedError


def build_qa_chain_with_sources(
    llm: BaseChatModel,
    prompt: ChatPromptTemplate,
) -> Runnable:
    """Build a Q&A chain that also returns which documents were used.

    Similar to build_qa_chain but the output includes both the answer
    and the source document indices that contributed to it.

    Args:
        llm: The language model to use.
        prompt: The prompt template.

    Returns:
        An LCEL Runnable returning {"answer": str, "source_indices": list[int]}.
    """
    # TODO: Implement
    # 1. Build the base QA chain
    # 2. Add a parallel branch that passes through the original documents
    # 3. Parse the LLM output to extract source references
    raise NotImplementedError
