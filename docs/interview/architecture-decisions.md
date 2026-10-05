# Architecture Decisions

- **Why LangChain?** It provides a common typed interface for tools, models, prompt templates, and retrievers. The demo already wraps customer-scoped reads as LangChain tools.
- **Why LangGraph?** It owns explicit workflow state, node transitions, conditional control flow, retries, and checkpoint integration rather than leaving coordination to uncontrolled chat calls.
- **Why multi-agent?** Separate intent, planning, routing, specialist access, resolution, critique, and validation boundaries make permissions and evidence checks auditable.
- **Why RAG and pgvector?** Policies change independently from code. Metadata-filtered retrieval can ground responses in authorized, citable document chunks; pgvector stores embeddings alongside relational metadata.
- **Why Redis?** It can support rate limits, ephemeral conversation state, and fast coordination; durable workflow recovery should use a persistent LangGraph checkpointer.
- **Why FastAPI and PostgreSQL?** FastAPI provides typed async-friendly HTTP endpoints; PostgreSQL supports transactional order/ticket data and relational auditability.
- **Why tool calling?** Order data and consequential operations must go through narrow, permission-checked interfaces rather than direct model database access.
- **How do routing and memory work?** Intent and deterministic rules select a specialist in the graph. The current demo keeps workflow state in memory only; production should scope conversation memory to the customer and persist graph checkpoints with retention controls.
- **How are hallucinations and prompt injection reduced?** Only verified tool data and retrieved evidence support outcomes; missing evidence fails closed. Inputs and retrieved text are untrusted. The current injection filter is intentionally minimal and must be replaced before production.
- **How does escalation and recovery work?** Explicit human requests produce a handoff outcome; production should add ticket creation, approval interrupts, checkpoint persistence, bounded retries, and failure queues.

The checked-in implementation is a local foundation, not a claim that database persistence, semantic RAG, model calls, or production identity are already enabled.