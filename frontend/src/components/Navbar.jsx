import { Bell, LogOut, Menu, Search, ShieldCheck } from 'lucide-react'

export default function Navbar({ onMenu, user, onLogout }) {
  return (
    <header className="navbar">
      <button className="icon-button mobile-menu" onClick={onMenu} aria-label="Open navigation"><Menu size={21} /></button>
      <div className="search-box">
        <Search size={18} />
        <input aria-label="Search security data" placeholder="Search threats, IPs, assets…" />
        <kbd>⌘ K</kbd>
      </div>
      <div className="navbar-actions">
        <span className="live-indicator"><i /> Live telemetry</span>
        <button className="icon-button notification-button" aria-label="Notifications"><Bell size={19} /><span /></button>
        <div className="analyst-profile">
          <div className="avatar"><ShieldCheck size={19} /></div>
          <div><strong>{user?.username || 'SOC Analyst'}</strong><small>{user?.role || 'Analyst'}</small></div>
        </div>
        <button className="icon-button" onClick={onLogout} aria-label="Sign out" title="Sign out"><LogOut size={17}/></button>
      </div>
    </header>
  )
}
