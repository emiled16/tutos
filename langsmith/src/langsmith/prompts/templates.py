"""Prompt template definitions for different Q&A strategies.

Each template is a ChatPromptTemplate with placeholders for "context"
(the retrieved documents) and "question" (the user's query).
"""

from langchain_core.prompts import ChatPromptTemplate


CONCISE_QA_TEMPLATE = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant. Answer the question based only on the "
        "provided context. Be concise — aim for 1-3 sentences.",
    ),
    (
        "human",
        "Context:\n{context}\n\nQuestion: {question}",
    ),
])

DETAILED_QA_TEMPLATE = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a thorough research assistant. Answer the question based only "
        "on the provided context. Provide a comprehensive answer with supporting "
        "details. If relevant, mention caveats or limitations.",
    ),
    (
        "human",
        "Context:\n{context}\n\nQuestion: {question}\n\n"
        "Please provide a detailed answer:",
    ),
])

STEP_BY_STEP_QA_TEMPLATE = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an analytical assistant. Answer the question based only on "
        "the provided context. Think through the problem step by step before "
        "giving your final answer.",
    ),
    (
        "human",
        "Context:\n{context}\n\nQuestion: {question}\n\n"
        "Let's work through this step by step:",
    ),
])


def get_all_templates() -> dict[str, ChatPromptTemplate]:
    """Return a mapping of template name to ChatPromptTemplate.

    Returns:
        Dict with keys "concise", "detailed", "step_by_step" mapped
        to their respective templates.
    """
    # TODO: Implement — return the dict of all templates defined above
    raise NotImplementedError


def get_template_descriptions() -> dict[str, str]:
    """Return human-readable descriptions for each template.

    Returns:
        Dict mapping template names to their descriptions.
    """
    # TODO: Implement — return descriptions for each template strategy
    raise NotImplementedError
