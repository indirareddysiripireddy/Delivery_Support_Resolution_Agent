import Link from "next/link";
import { ArrowLeft, PackageCheck } from "lucide-react";

export default async function OrderDetailPage({ params }: { params: Promise<{ orderId: string }> }) {
  const { orderId } = await params;
  const isFirstOrder = orderId === "DS-1001";
  const item = isFirstOrder ? "Wireless headphones" : "Desk lamp";
  const status = isFirstOrder ? "Delivered" : "In transit";
  return <div className="page-wrap"><div className="page-heading"><div><div className="eyebrow">ORDER DETAILS</div><h1>{orderId}</h1><p className="page-subtitle">{item} · Local demo record</p></div><Link className="button-secondary" href="/orders"><ArrowLeft size={14} /> All orders</Link></div><section className="section context-section"><div className="context-heading"><PackageCheck size={16} /> Delivery status</div><span className={`status-pill ${status === "In transit" ? "pending" : ""}`}>{status}</span><div className="data-pair"><span>Item</span><b>{item}</b></div><div className="data-pair"><span>Carrier</span><b>ParcelPost</b></div><div className="data-pair"><span>Tracking reference</span><b>{isFirstOrder ? "PP-DEMO-1001" : "PP-DEMO-1002"}</b></div>{isFirstOrder && <div className="data-pair"><span>Recorded delivered</span><b>Oct 04, 2026 · 14:32 UTC</b></div>}</section><p className="page-subtitle" style={{ marginTop: 14 }}>This page displays sample data only. Use support chat for policy-grounded help.</p></div>;
}