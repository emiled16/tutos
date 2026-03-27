"""Document summarization chain using LangChain.

Supports both single-document summarization and iterative
map-reduce summarization for long documents.
"""

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable


SUMMARIZATION_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a precise summarizer. Condense the following text into a clear, "
        "concise summary that captures all key points. Maintain factual accuracy.",
    ),
    ("human", "Summarize the following document:\n\n{document}"),
])


def build_summarization_chain(
    llm: BaseChatModel,
    prompt: ChatPromptTemplate | None = None,
) -> Runnable:
    """Build an LCEL chain for document summarization.

    Args:
        llm: The language model to use.
        prompt: Optional custom prompt. Uses SUMMARIZATION_PROMPT if not provided.

    Returns:
        An LCEL Runnable that accepts {"document": str} and returns a summary string.
    """
    # TODO: Implement
    # 1. Use the provided prompt or fall back to SUMMARIZATION_PROMPT
    # 2. Chain: prompt -> llm -> StrOutputParser
    raise NotImplementedError


def build_map_reduce_chain(
    llm: BaseChatModel,
    chunk_size: int = 2000,
) -> Runnable:
    """Build a map-reduce summarization chain for long documents.

    Splits the document into chunks, summarizes each chunk individually,
    then produces a final combined summary.

    Args:
        llm: The language model to use.
        chunk_size: Maximum character count per chunk.

    Returns:
        An LCEL Runnable that accepts {"document": str} and returns a summary string.
    """
    # TODO: Implement
    # 1. Create a text splitter to chunk the document
    # 2. Map step: summarize each chunk independently
    # 3. Reduce step: combine chunk summaries into a final summary
    raise NotImplementedError
