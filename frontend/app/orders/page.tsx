import Link from "next/link";
import { ArrowRight, Package } from "lucide-react";

const orders = [
  { id: "DS-1001", item: "Wireless headphones", status: "Delivered", date: "Oct 04, 2026" },
  { id: "DS-1002", item: "Desk lamp", status: "In transit", date: "Oct 05, 2026" },
];

export default function OrdersPage() {
  return <div className="page-wrap"><div className="page-heading"><div><div className="eyebrow">YOUR ACCOUNT</div><h1>Orders</h1><p className="page-subtitle">Recent sample orders in the local demo account.</p></div></div><div className="section"><div className="table-head"><span>ORDER</span><span>ITEM</span><span>STATUS</span><span>DATE</span></div>{orders.map((order) => <div className="order-row" key={order.id}><div className="order-name"><Link className="order-link" href={`/orders/${order.id}`}>{order.id} <ArrowRight size={12} /></Link></div><span className="order-detail">{order.item}</span><span className={`status-pill ${order.status === "In transit" ? "pending" : ""}`}><Package size={11} />{order.status}</span><span className="order-detail">{order.date}</span></div>)}</div></div>;
}