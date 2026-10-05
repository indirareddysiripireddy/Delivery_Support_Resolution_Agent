import type { Metadata } from "next";
import Link from "next/link";
import { Activity, ArrowUpRight, ClipboardList, Headphones, LayoutDashboard, Package, Settings } from "lucide-react";
import "./globals.css";

export const metadata: Metadata = {
  title: "Parcel Desk | Delivery Support",
  description: "Customer delivery support workspace",
};

const navigation = [
  { href: "/", label: "Overview", icon: LayoutDashboard },
  { href: "/chat", label: "Support chat", icon: Headphones },
  { href: "/orders", label: "Orders", icon: Package },
  { href: "/tickets", label: "Tickets", icon: ClipboardList },
  { href: "/analytics", label: "Activity", icon: Activity },
  { href: "/settings", label: "Settings", icon: Settings },
];

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <div className="app-frame">
          <aside className="sidebar">
            <Link href="/" className="brand-lockup">
              <span className="brand-mark"><Package size={18} strokeWidth={2.2} /></span>
              <span><strong>Parcel Desk</strong><small>DELIVERY SUPPORT</small></span>
            </Link>
            <div className="workspace-label">WORKSPACE</div>
            <nav className="main-nav" aria-label="Main navigation">
              {navigation.map(({ href, label, icon: Icon }) => (
                <Link className="nav-link" href={href} key={href}>
                  <Icon size={17} strokeWidth={1.8} />{label}
                </Link>
              ))}
            </nav>
            <div className="sidebar-bottom">
              <div className="online-indicator"><span /> Demo systems operational</div>
              <div className="profile-row"><div className="avatar">JD</div><div><strong>Jordan Davis</strong><small>Customer account</small></div><ArrowUpRight size={15} /></div>
            </div>
          </aside>
          <main className="main-content">{children}</main>
        </div>
      </body>
    </html>
  );
}