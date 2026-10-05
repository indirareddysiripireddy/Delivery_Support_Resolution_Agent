import Link from "next/link";
import { ArrowRight, ShieldCheck } from "lucide-react";

export default function LoginPage() {
  return <div className="page-wrap" style={{ maxWidth: 520, paddingTop: 56 }}><div className="eyebrow">LOCAL DEVELOPMENT</div><h1>Welcome to Parcel Desk.</h1><p className="page-subtitle" style={{ lineHeight: 1.7, margin: "14px 0 24px" }}>This starter uses a single configured demo bearer token. It does not provide customer account registration or production identity verification.</p><section className="section context-section"><div className="context-heading"><ShieldCheck size={16} /> Demo access</div><p className="empty-context">Start the API with the same <code>DEMO_ACCESS_TOKEN</code> configured in the frontend environment. The browser chat uses that token only for local demonstration.</p><Link className="button-primary" href="/" style={{ marginTop: 18 }}>Continue to demo <ArrowRight size={14} /></Link></section></div>;
}