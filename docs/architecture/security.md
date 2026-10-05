# Security Boundaries

- Every chat request requires a bearer token. The local verifier maps the one demo token to `cust_demo`; it is deliberately rejected when `APP_ENV=production`.
- Order tools require both order ID and authenticated customer ID, and return no data for unknown or cross-customer IDs.
- Tool operations are read-only in this starter. Refunds, cancellations, and replacements are represented as human-review outcomes and are never executed.
- Input size is limited and a small set of direct prompt-extraction patterns is blocked. This is a demo guardrail, not a comprehensive prompt-injection detector.
- Policy text is treated as evidence, not executable instructions. Responses cite a local source and do not expose workflow internals.
- The browser demo token is public by design. It has no production security value; replace the login and identity layer before any deployment.

Production needs strong identity and RBAC, tenant isolation at every repository and retrieval layer, robust injection/PII/secret controls, tool schemas and audit events, human approval for risky actions, secret management, rate limits, retention policies, tracing, and adversarial testing.