# System Architecture

The current runnable slice is a Next.js App Router UI, a FastAPI API, and a LangGraph-managed support workflow. The workflow checks authenticated demo identity against local order fixtures, loads an intent-specific policy document, produces a structured conservative outcome, validates the outcome, and returns only customer-safe status and evidence.

```text
Next.js chat -> FastAPI bearer-authenticated endpoint -> LangGraph
  -> guardrail -> intent -> supervisor/planner/router -> scoped tools
  -> local policy evidence -> resolution -> critic -> validator -> response
```

PostgreSQL/pgvector and Redis are available in Compose for future persistence and checkpoint integration. The current demo does not connect to them, persist conversations, stream responses, or call a model. The fixture adapters are not production order, identity, or policy systems.

## Production integration boundary

Before deployment, replace demo authentication and in-memory fixtures with a verified identity provider and customer-scoped repositories; persist workflow/checkpoint/audit data under retention controls; implement migrations and tenant-aware vector retrieval; add approved transactional tools and human approval; configure rate limiting, observability, and model-provider secrets; and add integration/e2e tests against controlled services. Do not expose the default token or sample policies to customers.