import Link from "next/link";
import { ArrowRight, CircleHelp, Clock3, MessageCircle, Package, ShieldCheck } from "lucide-react";

const demoOrders = [
  { id: "DS-1001", item: "Wireless headphones", date: "Oct 04, 2026", status: "Delivered", kind: "" },
  { id: "DS-1002", item: "Desk lamp", date: "Oct 05, 2026", status: "In transit", kind: "pending" },
];

export default function DashboardPage() {
  return (
    <div className="page-wrap">
      <div className="page-heading">
        <div><div className="eyebrow">MONDAY, OCTOBER 5</div><h1>Your deliveries, in view.</h1><p className="page-subtitle">A clear view of your recent orders and support requests.</p></div>
        <Link className="button-primary" href="/chat"><MessageCircle size={15} /> Get delivery help</Link>
      </div>
      <div className="notice">Demo workspace · Order and policy information shown here is local sample data.</div>
      <section className="metrics-grid" aria-label="Account overview">
        <Metric icon={<Package size={15} />} label="Recent orders" value="02" note="In this demo account" />
        <Metric icon={<Clock3 size={15} />} label="On the way" value="01" note="DS-1002 · Desk lamp" />
        <Metric icon={<CircleHelp size={15} />} label="Open requests" value="00" note="No saved support tickets" />
        <Metric icon={<ShieldCheck size={15} />} label="Account status" value="Ready" note="Demo identity verified" />
      </section>
      <div className="content-grid">
        <section className="section">
          <div className="section-header"><h2>Recent orders</h2><Link href="/orders">View all <ArrowRight size={13} /></Link></div>
          {demoOrders.map((order) => <div className="order-row" key={order.id}>
            <div className="order-name"><strong>{order.item}</strong><small>{order.id}</small></div>
            <span className="order-detail">{order.date}</span>
            <span className={`status-pill ${order.kind}`}><span>●</span>{order.status}</span>
          </div>)}
        </section>
        <section className="section">
          <div className="section-header"><h2>Support shortcuts</h2></div>
          <div className="activity-list">
            <div className="activity-item"><div className="activity-dot" /><div><strong>Check a delivery</strong><p>See verified order status and carrier details.</p><Link href="/chat" className="order-link">Start a chat →</Link></div></div>
            <div className="activity-item"><div className="activity-dot" /><div><strong>Ask about a policy</strong><p>Get guidance grounded in the support documents.</p><Link href="/chat" className="order-link">Ask support →</Link></div></div>
          </div>
        </section>
      </div>
    </div>
  );
}

function Metric({ icon, label, value, note }: { icon: React.ReactNode; label: string; value: string; note: string }) {
  return <div className="metric"><div className="metric-top"><span>{label}</span><span className="metric-icon">{icon}</span></div><p className="metric-value">{value}</p><p className="metric-note">{note}</p></div>;
}