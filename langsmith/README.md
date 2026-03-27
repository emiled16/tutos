# LLM Evaluation Pipeline

Build an LLM-powered Q&A system with comprehensive LangSmith tracing, custom evaluators, dataset-based testing, prompt versioning, and A/B testing of different prompt strategies.

## Overview

This project teaches you how to build production-grade LLM applications with full observability and systematic evaluation. You will construct a document Q&A system instrumented with LangSmith tracing, create custom evaluators to measure response quality across multiple dimensions, manage prompt templates with versioning, and run comparative evaluations to identify the best prompt strategies.

## Learning Objectives

- Instrument LLM applications with LangSmith for end-to-end tracing and observability
- Design and implement custom evaluators (correctness, relevance, faithfulness, toxicity)
- Create and manage evaluation datasets in LangSmith
- Build a prompt registry with versioning and A/B testing capabilities
- Run systematic evaluations comparing prompt strategies against datasets
- Understand LangChain's callback system and how to extend it
- Implement metadata tagging for filtering and analyzing runs in LangSmith

## Project Description

You are building a Q&A system that answers questions over a collection of documents. The system includes:

1. **Q&A Chain** — A retrieval-augmented generation (RAG) chain that retrieves relevant document chunks and generates answers
2. **Summarization Chain** — A chain for condensing long documents into concise summaries
3. **Prompt Registry** — A versioned collection of prompt templates (concise, detailed, step-by-step) that can be swapped and compared
4. **Custom Evaluators** — LangSmith evaluators that score outputs on correctness, relevance, faithfulness to source material, and toxicity
5. **Dataset Manager** — Utilities for creating, uploading, and managing evaluation datasets in LangSmith
6. **Evaluation Runner** — An orchestrator that runs chains against datasets using different prompt versions and compares results
7. **Tracing & Metadata** — Custom callback handlers and metadata utilities for enriching LangSmith traces

## Architecture

```
src/langsmith/
├── app.py                          # Main application entry point
├── chains/
│   ├── qa_chain.py                 # RAG Q&A chain
│   └── summarization_chain.py      # Document summarization chain
├── prompts/
│   ├── prompt_registry.py          # Prompt template management & versioning
│   └── templates.py                # Prompt template definitions
├── evaluation/
│   ├── evaluators.py               # Custom LangSmith evaluators
│   ├── dataset_manager.py          # LangSmith dataset CRUD operations
│   └── runner.py                   # Evaluation orchestration
└── tracing/
    ├── callbacks.py                # Custom LangSmith callback handlers
    └── metadata.py                 # Run metadata & tagging utilities

tests/
├── test_evaluators.py
├── test_chains.py
└── test_prompt_registry.py
```

## Implementation Tasks

### Phase 1: Core Chains
- [ ] Implement the Q&A chain with document retrieval (`chains/qa_chain.py`)
- [ ] Implement the summarization chain (`chains/summarization_chain.py`)
- [ ] Wire up the main application entry point (`app.py`)

### Phase 2: Prompt Management
- [ ] Define prompt templates for different strategies (`prompts/templates.py`)
- [ ] Build the prompt registry with versioning support (`prompts/prompt_registry.py`)

### Phase 3: Tracing & Observability
- [ ] Implement custom callback handlers for detailed tracing (`tracing/callbacks.py`)
- [ ] Build metadata and tagging utilities (`tracing/metadata.py`)

### Phase 4: Evaluation
- [ ] Create custom evaluators for correctness, relevance, faithfulness, toxicity (`evaluation/evaluators.py`)
- [ ] Implement dataset management utilities (`evaluation/dataset_manager.py`)
- [ ] Build the evaluation runner to compare prompt versions (`evaluation/runner.py`)

### Phase 5: Testing
- [ ] Write tests for all custom evaluators
- [ ] Write tests for chain construction and invocation
- [ ] Write tests for prompt registry operations

## Evaluation Criteria

- All chains produce correct outputs when traced in LangSmith
- Custom evaluators return well-structured scores with reasoning
- Prompt registry supports CRUD operations and version history
- Evaluation runner produces comparison reports across prompt versions
- Traces appear in LangSmith with correct metadata and tags
- Tests pass with `pytest`

## Resources

- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [LangChain Expression Language (LCEL)](https://python.langchain.com/docs/expression_language/)
- [LangSmith Evaluation Guide](https://docs.smith.langchain.com/evaluation)
- [LangSmith Cookbook](https://github.com/langchain-ai/langsmith-cookbook)
- [LangChain Callbacks](https://python.langchain.com/docs/modules/callbacks/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
