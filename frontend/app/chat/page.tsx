"use client";

import { FormEvent, useState } from "react";
import { Check, CircleHelp, LoaderCircle, Package, Send, ShieldCheck, Sparkles } from "lucide-react";

type Evidence = { source: string; section: string; excerpt: string };
type Result = {
  status: string;
  response: string;
  order: Record<string, string> | null;
  delivery: Record<string, string> | null;
  evidence: Evidence[];
  workflow_status: string[];
};
type Message = { role: "user" | "assistant"; text: string; result?: Result };

const workflowLabels = ["Understanding request", "Checking order", "Checking delivery status", "Reviewing support policy", "Validating resolution", "Preparing customer response"];

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", text: "Hi Jordan. I can check a delivery, explain a support policy, or help route an issue. What can I look into?" },
  ]);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [active, setActive] = useState<Result | null>(null);
  const [error, setError] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const message = draft.trim();
    if (!message || busy) return;
    setMessages((current) => [...current, { role: "user", text: message }]);
    setDraft("");
    setBusy(true);
    setError("");
    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      if (!response.ok) throw new Error(response.status === 503 ? "Support is not configured for this deployment yet." : "Support could not process that request.");
      const result = await response.json() as Result;
      setActive(result);
      setMessages((current) => [...current, { role: "assistant", text: result.response, result }]);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to reach support right now.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="page-wrap">
      <div className="page-heading">
        <div><div className="eyebrow">SUPPORT</div><h1>Let’s sort it out.</h1><p className="page-subtitle">Share the order number and what happened. We’ll check verified details first.</p></div>
        <span className="status-pill"><span>●</span> Demo workspace</span>
      </div>
      <div className="chat-layout">
        <section className="section chat-panel" aria-label="Support chat">
          <div className="chat-header"><div className="chat-orb"><Sparkles size={17} /></div><div><strong>Delivery Support</strong><small>Order checks and policy-based guidance</small></div></div>
          <div className="chat-stream" aria-live="polite">
            {messages.map((message, index) => <div className={`chat-message ${message.role}`} key={`${index}-${message.text.slice(0, 12)}`}>
              <div className="message-label">{message.role === "user" ? "YOU" : "PARCEL DESK"}</div>
              <div className="message-bubble">{message.text}</div>
            </div>)}
            {busy && <div className="chat-message assistant"><div className="message-label">PARCEL DESK</div><div className="message-bubble"><LoaderCircle className="animate-spin" size={15} /> Checking the order and support guidance…</div></div>}
          </div>
          <form className="chat-composer" onSubmit={submit}>
            <div className="composer-row"><textarea aria-label="Message support" maxLength={4000} onChange={(event) => setDraft(event.target.value)} onKeyDown={(event) => { if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); event.currentTarget.form?.requestSubmit(); } }} placeholder="For example: My order DS-1001 says delivered but I didn't receive it." value={draft} /><button aria-label="Send message" disabled={busy || !draft.trim()} type="submit"><Send size={16} /></button></div>
            {error ? <p className="error-note">{error}</p> : <p className="composer-hint">Enter to send · Shift + Enter for a new line</p>}
          </form>
        </section>
        <aside className="context-panel" aria-label="Support details">
          <section className="section context-section"><div className="context-heading"><Package size={15} /> Order details</div>
            {active?.order ? <><strong>{active.order.item_summary}</strong><div className="data-pair"><span>Order</span><b>{active.order.order_id}</b></div><div className="data-pair"><span>Order status</span><b>{active.order.status}</b></div><div className="data-pair"><span>Total</span><b>{active.order.currency} {active.order.total}</b></div>{active.delivery && <div className="data-pair"><span>Carrier status</span><b>{active.delivery.status}</b></div>}</> : <p className="empty-context">Verified order information will appear here when a matching order is checked.</p>}
          </section>
          <section className="section context-section"><div className="context-heading"><ShieldCheck size={15} /> Policy evidence</div>
            {active?.evidence.length ? active.evidence.map((item) => <div className="evidence-card" key={item.source}><strong>{item.section}</strong><p>{item.excerpt}</p><p>Source: {item.source}</p></div>) : <p className="empty-context">Relevant support guidance will be shown with its source.</p>}
          </section>
          <section className="section context-section"><div className="context-heading"><CircleHelp size={15} /> Request progress</div>
            <ul className="workflow-list">{workflowLabels.map((label) => { const done = active?.workflow_status.includes(label) ?? false; return <li className={done ? "done" : ""} key={label}><span className="workflow-check">{done && <Check size={10} />}</span>{label}</li>; })}</ul>
          </section>
          <div className="notice">A refund, replacement, or cancellation is never approved automatically in this demo.</div>
        </aside>
      </div>
    </div>
  );
}