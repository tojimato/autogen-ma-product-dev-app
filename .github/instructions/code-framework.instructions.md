---
applyTo: "**"
---
# Framework Specification: AutoGen AgentChat (v0.4.x)

This document defines technical standards for designing multi-agent systems in this project using the AutoGen AgentChat (v0.4.x) library. In addition to the main coding rules, the following framework-specific rules must be applied:

## 1. Architectural Layers
- **AgentChat API Usage:** Build the project on the higher-level, intuitive AgentChat API, not the low-level autogen-core.
- **Asynchronous Design:** All agent methods (`run`, `run_stream`, `on_messages`) must be designed and called asynchronously.
- **Typing:** Use framework-specific types such as `BaseChatMessage`, `TaskResult`, and `StopMessage`.

## 2. Agent Definition Standards
- **AssistantAgent:** Use the `AssistantAgent` class for general tasks requiring LLM and tool usage.
- **Attributes:** Every agent must have a unique `name` and a `description` explaining its function; these are critical for team coordination.
- **State Management:** Use `save_state()` and `load_state()` methods to persist and restore agent state.
- **Custom Agents:** If built-in agents are insufficient, subclass `BaseChatAgent` and implement `on_messages`, `on_reset`, and `produced_message_types` methods.

## 3. Team Coordination & Workflows
Choose the appropriate team structure based on task complexity:
- **RoundRobinGroupChat:** For simple cyclic structures where agents speak in a fixed order.
- **SelectorGroupChat:** For dynamic speaker selection by an LLM based on context.
- **Swarm:** For decentralized handoff-based workflows using `HandoffMessage`.
- **GraphFlow:** For deterministic workflows, build directed graphs with `DiGraphBuilder`.

## 4. Tools & Memory
- **Functional Tools:** When providing Python functions as tools, ensure proper docstrings; `AssistantAgent` will auto-generate schemas.
- **Parallel Tool Calls:** When using `AgentTool` or `TeamTool`, set `parallel_tool_calls=False` in the model client to prevent state conflicts.
- **Memory Protocol:** Integrate `ListMemory` or `ChromaDBVectorMemory` for RAG and context management.

## 5. Termination Conditions
Control workflows using these conditions with `|` (OR) or `&` (AND) operators:
- **MaxMessageTermination:** Maximum message limit.
- **TextMentionTermination("TERMINATE"):** Stop on a specific keyword.
- **HandoffTermination(target="user"):** Handover control to the user.

## 6. Observability
- **Logging:** Configure Python logging via `autogen_agentchat.EVENT_LOGGER_NAME` to monitor events.
- **Tracing:** Follow OpenTelemetry and Jaeger integration standards for advanced tracing.

---

**Note:** This file works in conjunction with the project's general Clean Code rules. If a framework-specific detail conflicts with the main rules, the framework specification takes precedence.