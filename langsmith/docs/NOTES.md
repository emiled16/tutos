# LLM Evaluation Pipeline — Theory & Notes

## LLM Observability

### Why Observability Matters

LLM applications are non-deterministic by nature. The same input can produce different outputs across runs. Without observability, debugging failures, understanding performance regressions, and optimizing prompts becomes guesswork.

Key concerns:
- **Latency tracking** — Which parts of the chain are slow?
- **Token usage** — How much does each call cost?
- **Error correlation** — When a chain fails, which sub-step caused it?
- **Quality drift** — Are responses degrading over time?

### Tracing and Spans

A **trace** is a record of a single end-to-end execution of your LLM application. Each trace is composed of **spans** (also called "runs" in LangSmith):

- **Chain runs** — The top-level orchestration
- **LLM runs** — Individual calls to language models
- **Tool runs** — External tool invocations (search, calculator, etc.)
- **Retriever runs** — Document retrieval operations

Each span captures: inputs, outputs, latency, token counts, metadata, and error information.

LangSmith automatically nests spans to show the parent-child relationship, making it easy to see how data flows through your application.

## Evaluation Methodologies for LLMs

### Reference-Based Evaluation

Compare the model's output against a known correct answer (ground truth). Works well for factual Q&A where there's a definitive answer.

- **Exact match** — Binary: does the output match the reference?
- **Semantic similarity** — Embedding-based comparison (cosine similarity)
- **ROUGE/BLEU** — N-gram overlap metrics borrowed from machine translation

Limitation: Many valid answers exist for open-ended questions. Reference-based metrics can penalize correct but differently-worded responses.

### Reference-Free Evaluation

Evaluate the output without a ground truth answer. Useful for creative tasks, summarization, or when ground truth is unavailable.

- **Fluency** — Is the output grammatically correct and readable?
- **Coherence** — Does the output logically flow?
- **Relevance** — Does the output address the input question?

### LLM-as-Judge

Use a (typically stronger) LLM to evaluate another LLM's output. This is the most flexible approach and can handle nuanced quality dimensions.

Common patterns:
- **Single-point scoring** — Rate on a scale of 1-5 with reasoning
- **Pairwise comparison** — Which of two outputs is better?
- **Criteria-based rubrics** — Score against specific criteria (accuracy, completeness, tone)

Considerations:
- Judge model bias (position bias, verbosity bias)
- Cost of running a judge model on every evaluation
- Need for calibration against human judgments

## Dataset Creation Strategies

### Manual Curation

Hand-craft input/output pairs that cover important scenarios:
- Happy path cases
- Edge cases (empty input, very long input, ambiguous questions)
- Adversarial cases (prompt injection attempts, off-topic queries)

### Production Sampling

Sample real user interactions and annotate them:
- Filter for diverse query types
- Have domain experts label ground truth
- Include cases where the system failed

### Synthetic Generation

Use an LLM to generate evaluation examples:
- Provide a document and ask the LLM to generate questions about it
- Use chain-of-thought to generate plausible wrong answers as negative examples
- Validate synthetic data with human review

### Dataset Size Guidelines

- **Minimum viable**: 20-50 examples for initial development
- **Robust evaluation**: 100-200 examples covering key scenarios
- **Statistical significance**: 500+ examples for reliable A/B comparisons

## Prompt Engineering Best Practices

### Few-Shot vs Zero-Shot

**Zero-shot**: The model receives only the task instruction, no examples.
- Pro: Simple, no example curation needed
- Con: Less control over output format and quality

**Few-shot**: The model receives task instruction plus 2-5 examples.
- Pro: Better format compliance, higher quality for specific tasks
- Con: Consumes tokens, examples must be representative

### Chain of Thought (CoT)

Instruct the model to "think step by step" before producing an answer. This improves performance on reasoning-heavy tasks.

Variants:
- **Zero-shot CoT**: Simply add "Let's think step by step" to the prompt
- **Few-shot CoT**: Provide examples that include reasoning steps
- **Self-consistency**: Generate multiple CoT paths and take the majority answer

### Systematic Prompt Iteration Workflow

1. **Baseline** — Start with a simple, clear prompt
2. **Evaluate** — Run against a test dataset, measure key metrics
3. **Error analysis** — Examine failure cases, categorize error types
4. **Hypothesize** — Form a theory about why failures happen
5. **Iterate** — Modify the prompt to address the specific failure mode
6. **Re-evaluate** — Run against the same dataset, compare metrics
7. **Version** — Save the prompt with a version number and evaluation results

Never change multiple things at once. Iterate on one dimension at a time.

## LangSmith vs Alternatives

| Feature | LangSmith | Weights & Biases | MLflow |
|---------|-----------|-------------------|--------|
| LLM-specific tracing | Native | Via Prompts (W&B Weave) | Via plugins |
| LangChain integration | First-party | Community | Community |
| Custom evaluators | Yes, with SDK | Yes | Yes |
| Dataset management | Built-in | Via Artifacts | Via Datasets |
| Prompt versioning | Native Hub | Via Artifacts | Via Model Registry |
| Production monitoring | Yes | Yes | Limited |
| Pricing model | Per trace | Per tracked hour | Open-source / managed |
| Self-hosted option | Enterprise | No | Yes |

## Production Monitoring for LLMs

### Key Metrics to Track

- **Latency** (p50, p95, p99) — Response time distribution
- **Token usage** — Input/output tokens per request
- **Error rate** — Percentage of failed requests
- **Cost** — Dollar cost per request and per day
- **User feedback** — Thumbs up/down, corrections

### Feedback Loops

Production feedback is critical for continuous improvement:

1. **Explicit feedback** — Users rate responses (thumbs up/down)
2. **Implicit feedback** — Users copy the response, ask follow-ups, or abandon the conversation
3. **Annotation queues** — Route a sample of production traces to human reviewers
4. **Automated evaluation** — Run LLM-as-judge on production traces asynchronously

Feed this data back into your evaluation datasets to close the loop.

## Key Terminology

- **Trace** — A complete record of an LLM application execution
- **Span / Run** — A single operation within a trace (LLM call, retrieval, etc.)
- **Evaluator** — A function that scores an LLM output on a specific dimension
- **Dataset** — A collection of input/output pairs for evaluation
- **Prompt template** — A parameterized string used to construct LLM inputs
- **RAG** — Retrieval-Augmented Generation: grounding LLM answers in retrieved documents
- **LCEL** — LangChain Expression Language for composing chains declaratively
- **Callback handler** — A hook that receives events during chain execution
- **Few-shot** — Providing examples in the prompt to guide the model
- **Chain of Thought** — Prompting the model to show intermediate reasoning steps
- **LLM-as-Judge** — Using an LLM to evaluate another LLM's output
