import Link from "next/link";
import { ClipboardList, MessageCircle } from "lucide-react";

export default function TicketsPage() {
  return <div className="page-wrap"><div className="page-heading"><div><div className="eyebrow">SUPPORT HISTORY</div><h1>Support requests</h1><p className="page-subtitle">Human follow-ups are not persisted in this local demo.</p></div></div><section className="section context-section"><div className="context-heading"><ClipboardList size={16} /> No saved requests</div><p className="empty-context">Start a support conversation to check an order or request a human follow-up. Ticket persistence will be connected in a later integration.</p><Link className="button-primary" href="/chat" style={{ marginTop: 17 }}><MessageCircle size={14} /> Contact support</Link></section></div>;
}