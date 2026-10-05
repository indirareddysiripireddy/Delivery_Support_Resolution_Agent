# Vercel Deployment

The Next.js frontend can be deployed as a Vercel project with the project root set to `frontend/`. The API remains a separate FastAPI service; Vercel does not deploy the current Compose stack as one application.

1. Import the repository in Vercel and set **Root Directory** to `frontend`.
2. Configure server-only environment variables `DELIVERY_SUPPORT_API_URL` (the deployed API base URL ending in `/api/v1`) and `DELIVERY_SUPPORT_API_TOKEN` (a secret bearer token). Do not use `NEXT_PUBLIC_` for credentials.
3. Deploy the project. The chat UI calls the same-origin `/api/chat` route, which validates message size and forwards requests server-side.

## Important limitations

The current FastAPI authentication is demo-only and intentionally returns HTTP 503 when `APP_ENV=production`. It maps the single configured token to one sample customer and is not suitable for real customer accounts. Do not work around this by exposing the token, setting production to local mode for real customer data, or putting secrets in Vercel client-visible variables. For a public sample demo, use only synthetic data and add rate limiting before enabling the proxy. For a real deployment, implement customer identity/session authentication and tenant-aware API authorization first, deploy FastAPI separately, then configure the proxy to forward verified per-user identity rather than a shared demo credential.

Vercel deployment requires an authenticated Vercel account/CLI; no Vercel CLI or linked project is currently configured in this workspace.