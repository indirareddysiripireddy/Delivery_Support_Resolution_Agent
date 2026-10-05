import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";

export async function POST(request: NextRequest) {
  const apiUrl = process.env.DELIVERY_SUPPORT_API_URL
    ?? (process.env.NODE_ENV === "development" ? "http://localhost:8000/api/v1" : undefined);
  const apiToken = process.env.DELIVERY_SUPPORT_API_TOKEN
    ?? (process.env.NODE_ENV === "development" ? "dev-demo-token" : undefined);
  if (!apiUrl || !apiToken) {
    return NextResponse.json({ detail: "Support API is not configured." }, { status: 503 });
  }

  const body: unknown = await request.json().catch(() => null);
  if (
    !body
    || typeof body !== "object"
    || !("message" in body)
    || typeof body.message !== "string"
    || body.message.trim().length === 0
    || body.message.length > 4000
  ) {
    return NextResponse.json({ detail: "A message between 1 and 4000 characters is required." }, { status: 422 });
  }

  try {
    const response = await fetch(`${apiUrl.replace(/\/$/, "")}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiToken}`,
      },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(20000),
      cache: "no-store",
    });
    const responseBody: unknown = await response.json().catch(() => ({ detail: "Support request failed." }));
    return NextResponse.json(responseBody, { status: response.status });
  } catch {
    return NextResponse.json({ detail: "Support service is unavailable." }, { status: 502 });
  }
}