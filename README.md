# Delivery Support Resolution Agent

A local-development foundation for a delivery-support resolution service. The core path is a typed LangGraph workflow: validate input, classify intent, plan and route, verify order and delivery data through scoped LangChain tools, retrieve policy evidence, draft and validate a resolution, then return a customer-safe response.

## Local quick start

Requirements: Python 3.11+ and Docker Compose (optional for the deterministic demo).

```bash
cp .env.example .env
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
uvicorn backend.app.main:app --reload
```

Open `http://localhost:8000/docs`. The demo endpoint uses a bearer token (`dev-demo-token` by default); send `Authorization: Bearer dev-demo-token` and `POST /api/v1/chat` with `{"message":"My order DS-1001 says delivered but I didn't receive it."}`. Demo records and policies are explicitly local fixtures, not a real order system or company policy.

Start the optional PostgreSQL/pgvector and Redis services with `docker compose up -d`. The current workflow uses local demo adapters and does not persist customer data; connection settings are included for the next integration slice. Never use the demo token or fixtures in production.

## Repository map

- `backend/`: FastAPI app, typed request/response schemas, authentication dependency, and API routes.
- `ai/`: LangGraph workflow, structured state, scoped LangChain tools, and deterministic policy retrieval.
- `knowledge_base/`: local sample policy evidence with explicit eligibility and escalation rules.
- `frontend/`: Next.js customer-support workspace.
- `tests/`: workflow and API behavior tests.
- `deployment/`: container build files; `docker-compose.yml` runs local dependencies.

The workflow never approves or executes refunds, cancellations, or replacements. Those consequential operations require verified eligibility, an authorized integration, and (where configured) human approval. When policy evidence or order data is missing, it asks for information or escalates instead of inventing facts.

## Verification

```bash
pytest
```

See `docs/architecture/system.md` and `docs/architecture/security.md` for workflow boundaries, demo limitations, and the production hardening checklist.