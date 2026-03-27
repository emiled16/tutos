# Research Agent Swarm — Multi-Agent Orchestration

## Overview

Build a multi-agent system where specialized agents (researcher, analyst, writer, critic) collaborate to produce comprehensive research reports. The system demonstrates agent communication, task delegation, conflict resolution, and result synthesis — core patterns used in production AI agent systems.

## Learning Objectives

- Design and implement a multi-agent architecture with distinct agent roles
- Build an inter-agent communication system using a message bus and typed protocols
- Implement orchestration strategies (sequential, parallel, hierarchical) using DAG-based workflows
- Manage shared and individual agent memory for context persistence
- Integrate external tools (web search, analysis) into agent capabilities
- Handle errors, retries, and conflict resolution across agents
- Evaluate and iterate on multi-agent output quality

## Project Description

You will build a "Research Agent Swarm" that accepts a research topic and produces a structured, comprehensive research report. The system consists of four specialized agents:

1. **Researcher** — gathers raw information from web sources using search tools
2. **Analyst** — processes and synthesizes gathered information, identifying patterns and key findings
3. **Writer** — produces structured, well-formatted report sections from analyzed data
4. **Critic** — reviews drafts, provides feedback, and requests revisions

An **Orchestrator** coordinates these agents through a configurable workflow DAG, routing messages between them, managing shared context, and ensuring the final output meets quality criteria.

## Architecture

```
┌─────────────┐
│ Orchestrator │──────── Workflow DAG
└──────┬──────┘
       │
  ┌────┴────┐
  │ Message │
  │   Bus   │
  └────┬────┘
       │
 ┌─────┼─────┬──────┐
 │     │     │      │
 ▼     ▼     ▼      ▼
Res.  Anl.  Wrt.  Crit.
 │     │     │      │
 ▼     ▼     ▼      ▼
Tools  ─── Shared Memory ───
```

Key design decisions:
- **Message bus** for decoupled agent-to-agent communication
- **DAG-based workflows** so task execution order is explicit and parallelizable
- **Shared memory** for cross-agent context; **agent memory** for per-agent state
- **Strategy pattern** for swapping orchestration approaches without changing agents

## Implementation Tasks

### Phase 1 — Foundations
- [ ] Define message types and communication protocols (`protocols.py`)
- [ ] Implement the message bus (`message_bus.py`)
- [ ] Build the abstract base agent with lifecycle hooks (`base_agent.py`)
- [ ] Implement shared and individual agent memory stores

### Phase 2 — Agents
- [ ] Implement the Researcher agent with web search tool integration
- [ ] Implement the Analyst agent with synthesis capabilities
- [ ] Implement the Writer agent for structured report generation
- [ ] Implement the Critic agent with feedback and scoring logic

### Phase 3 — Orchestration
- [ ] Build the DAG workflow engine (`dag.py`)
- [ ] Implement orchestration strategies (sequential, parallel, hierarchical)
- [ ] Wire up the Orchestrator to manage end-to-end report generation
- [ ] Add error handling, retries, and conflict resolution

### Phase 4 — Polish
- [ ] Add evaluation metrics for report quality
- [ ] Write comprehensive tests for all components
- [ ] Run end-to-end with a real research topic

## Evaluation Criteria

- Agents communicate exclusively through the message bus (no direct coupling)
- Workflow DAG correctly manages execution order and parallelism
- Shared memory is properly synchronized across agents
- Error handling covers agent failures, API timeouts, and malformed outputs
- Tests cover orchestration logic, individual agents, and communication
- The system produces a coherent multi-section research report

## Resources

- [LangChain Agents Documentation](https://python.langchain.com/docs/concepts/agents/)
- [LangGraph Multi-Agent Guide](https://langchain-ai.github.io/langgraph/)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [AutoGen](https://github.com/microsoft/autogen)
- [CrewAI](https://github.com/crewAIInc/crewAI)
- [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)
- [Building Effective Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents)
