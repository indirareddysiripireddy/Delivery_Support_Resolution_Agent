# LangGraph Workflow

`ai/langgraph/workflows/delivery_workflow.py` compiles a typed `DeliveryState` graph with explicit guardrail, intent, supervisor, planner, router, specialist, evidence retrieval, resolution, critic, validator, and response nodes. The only current conditional branches are unsafe-input short-circuiting and validation-to-response; the specialist never performs refunds, cancellations, or replacement writes.

The deterministic demo classifier is used so local tests need no API key and sample workflows are reproducible. A production deployment should add bounded retries, checkpoint persistence, cancellation/timeouts, structured model fallback for ambiguous intents, and an interrupt/resume approval node before enabling consequential tools.