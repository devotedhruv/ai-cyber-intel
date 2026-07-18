import { Activity, BellRing, FileBarChart, LayoutDashboard, Network, Radar, ScrollText, Settings, Shield, X } from 'lucide-react'
import { NavLink } from 'react-router-dom'

const nav = [
  { to: '/', label: 'Overview', icon: LayoutDashboard },
  { to: '/logs', label: 'Security logs', icon: ScrollText },
  { to: '/threats', label: 'Threat intelligence', icon: Radar },
  { to: '/alerts', label: 'Alerts & detections', icon: BellRing },
  { to: '/assets', label: 'Asset inventory', icon: Network },
  { to: '/reports', label: 'Reports', icon: FileBarChart },
  { to: '/settings', label: 'Settings', icon: Settings },
]

export default function Sidebar({ open, onClose }) {
  return <>
    <div className={`sidebar-backdrop ${open ? 'visible' : ''}`} onClick={onClose} />
    <aside className={`sidebar ${open ? 'open' : ''}`}>
      <div className="brand"><div className="brand-mark"><Shield size={25} /></div><div><strong>SENTINEL<span>AI</span></strong><small>Unified Security Platform</small></div><button className="close-sidebar" onClick={onClose}><X /></button></div>
      <p className="nav-label">Security operations</p>
      <nav>{nav.map(({ to, label, icon: Icon }) => <NavLink key={to} to={to} end={to === '/'} onClick={onClose}><Icon size={19} /><span>{label}</span></NavLink>)}</nav>
      <div className="sidebar-spacer" />
      <div className="system-chip"><Activity size={18} /><div><strong>Central API</strong><span><i /> Port 8100</span></div></div>
      <div className="sidebar-version">Platform v1.0 · Phases 1–9</div>
    </aside>
  </>
}
