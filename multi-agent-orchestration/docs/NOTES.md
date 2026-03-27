# Multi-Agent Orchestration — Theory & Notes

## 1. Multi-Agent System Architectures

### Centralized (Orchestrator Pattern)
A single orchestrator decides which agent runs, when, and with what input. Agents are passive — they execute when called and return results.

**Pros:** Simple control flow, easy to debug, deterministic ordering.
**Cons:** Single point of failure, orchestrator becomes a bottleneck, hard to scale.

### Decentralized (Choreography Pattern)
Agents communicate directly via events/messages. Each agent decides autonomously when to act based on messages it receives.

**Pros:** Resilient, scalable, agents can be added/removed independently.
**Cons:** Hard to reason about global state, emergent behavior can be unpredictable.

### Hierarchical
Combines both: a top-level orchestrator delegates to sub-orchestrators, each managing a group of agents. Common in complex workflows.

**Pros:** Scalable control, natural decomposition of complex tasks.
**Cons:** More complex to implement, requires clear hierarchy definition.

## 2. Agent Communication Patterns

### Direct Messaging
Agent A sends a message directly to Agent B. Simple but creates tight coupling.

### Broadcast
Agent publishes a message to all agents. Useful for status updates but generates noise.

### Publish/Subscribe (Pub/Sub)
Agents subscribe to message topics. Publishers don't need to know subscribers. This is the recommended pattern for decoupled systems.

### Message Bus
Centralized channel through which all messages flow. Enables logging, filtering, and routing. Good for debugging and monitoring.

```python
# Conceptual message flow
researcher.publish("research_complete", findings)
# Message bus routes to subscribers
analyst.on("research_complete", analyze)
```

## 3. Orchestration vs Choreography

| Aspect | Orchestration | Choreography |
|--------|--------------|--------------|
| Control | Centralized | Distributed |
| Coupling | Agents coupled to orchestrator | Agents coupled to message format |
| Debugging | Easier (single control point) | Harder (distributed state) |
| Flexibility | Change orchestrator logic | Change individual agents |
| Scalability | Limited by orchestrator | Better horizontal scaling |

**For this project:** We use orchestration with a message bus, giving us centralized control with loose coupling between agents.

## 4. Agent Roles and Specialization

Each agent should have:
- **A clear, bounded responsibility** — one agent, one job
- **A well-defined interface** — inputs it accepts, outputs it produces
- **Its own system prompt** — personality and instructions tuned for its role
- **Tool access** — only the tools relevant to its task

### Role Design Principles
- Agents should be **composable** (can be rearranged in different workflows)
- Agents should be **stateless per invocation** (state lives in memory stores)
- Agents should produce **structured outputs** (Pydantic models, not free text)

## 5. Shared vs Isolated Memory

### Shared Memory
A key-value or document store accessible by all agents. Used for:
- Research findings that multiple agents need
- The evolving report draft
- Global configuration and constraints

### Individual Agent Memory
Per-agent state including:
- Conversation history with the LLM
- Intermediate results and scratchpad
- Agent-specific configuration

### Best Practice
Use shared memory for **artifacts** (research, drafts, feedback) and individual memory for **reasoning traces** (chain-of-thought, tool call history).

## 6. Conflict Resolution Strategies

When agents disagree (e.g., critic rejects writer output):

1. **Iterative Refinement** — send feedback back, let agent revise (most common)
2. **Voting** — multiple agents vote on the best output
3. **Hierarchical Override** — a supervisor agent makes the final decision
4. **Consensus** — agents negotiate until all agree (expensive, rarely used)
5. **Threshold-Based** — accept output if quality score exceeds threshold

## 7. ReAct Pattern

**Re**asoning + **Act**ing. The agent alternates between:
1. **Thought** — reason about what to do next
2. **Action** — call a tool or produce output
3. **Observation** — process the result

```
Thought: I need to find recent papers on multi-agent systems
Action: search("multi-agent systems 2024 survey")
Observation: Found 5 relevant papers...
Thought: Let me extract key findings from the top result
Action: read_document(url)
...
```

This pattern gives the LLM structured "thinking time" and grounds its reasoning in real tool outputs.

## 8. Chain-of-Thought in Agents

Each agent benefits from structured reasoning:
- **Plan before acting** — outline steps before executing
- **Reflect after acting** — evaluate results before moving on
- **Self-correct** — if output doesn't meet criteria, revise

## 9. Tool Use by Agents

Agents extend LLM capabilities with tools:
- **Search tools** — web search, document retrieval
- **Analysis tools** — data processing, statistics
- **Code execution** — run Python for calculations
- **File I/O** — read/write documents

### Tool Design Principles
- Tools should have **clear descriptions** (the LLM uses these to decide when to call them)
- Tools should return **structured data** (not raw HTML)
- Tools should handle **errors gracefully** (return error messages, not exceptions)

## 10. Framework Comparison

### LangGraph
- Graph-based agent orchestration built on LangChain
- Explicit state machines with nodes and edges
- Best for: Complex, stateful multi-agent workflows
- Strengths: Fine-grained control, persistence, human-in-the-loop

### AutoGen (Microsoft)
- Conversation-driven multi-agent framework
- Agents communicate via chat messages
- Best for: Conversational agent teams, code generation
- Strengths: Easy setup, built-in code execution

### CrewAI
- Role-based agent framework with task delegation
- Declarative agent and task definitions
- Best for: Rapid prototyping of agent teams
- Strengths: Simple API, role-based design

### When to Build Custom (This Project)
Building from scratch teaches you what these frameworks abstract away: message routing, state management, error handling, and orchestration logic.

## 11. Error Handling and Recovery

### Common Failure Modes
- **LLM API errors** — rate limits, timeouts, malformed responses
- **Tool failures** — search API down, invalid results
- **Agent loops** — agent stuck in a reasoning cycle
- **Quality failures** — output doesn't meet criteria

### Recovery Strategies
- **Retry with backoff** — for transient API errors
- **Fallback agents** — secondary agent takes over on failure
- **Circuit breaker** — stop after N failures, escalate to human
- **Max iterations** — cap reasoning loops to prevent infinite cycles
- **Graceful degradation** — produce partial report if some agents fail

## 12. Evaluating Multi-Agent Outputs

### Report Quality Metrics
- **Factual accuracy** — claims supported by sources
- **Coverage** — topic adequately covered
- **Coherence** — logical flow between sections
- **Citation quality** — sources are relevant and reliable

### System Metrics
- **Latency** — total time to produce report
- **Token usage** — cost efficiency
- **Agent utilization** — are all agents contributing meaningfully?
- **Iteration count** — how many revision cycles needed?

## Key Terminology

| Term | Definition |
|------|-----------|
| **Agent** | An LLM-powered entity with a defined role, tools, and memory |
| **Orchestrator** | Central coordinator that manages agent execution order |
| **Message Bus** | Communication channel routing messages between agents |
| **DAG** | Directed Acyclic Graph defining task execution order |
| **ReAct** | Reasoning + Acting pattern for structured agent behavior |
| **Tool** | External capability (API, function) an agent can invoke |
| **Shared Memory** | State store accessible by all agents |
| **Choreography** | Decentralized coordination via events |

## Common Pitfalls

1. **Over-engineering agent roles** — start simple (2-3 agents), add more only when needed
2. **Unbounded agent loops** — always set max iteration limits
3. **Ignoring token costs** — multi-agent systems multiply LLM calls; monitor usage
4. **Tight coupling** — agents should communicate through interfaces, not implementation details
5. **No observability** — log every message, tool call, and decision for debugging
6. **Premature optimization** — get the pipeline working end-to-end first, then optimize
