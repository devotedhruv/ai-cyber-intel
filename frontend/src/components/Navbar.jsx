import { useEffect, useState } from 'react'
import { Bell, Check, LogOut, Menu, Search, ShieldCheck } from 'lucide-react'
import { alertApi, logApi, notificationApi } from '../api/api'

export default function Navbar({ onMenu, user, onLogout }) {
  const [counts,setCounts]=useState({threats:0,critical:0})
  const [notifications,setNotifications]=useState([])
  const [unread,setUnread]=useState(0)
  const [notificationsOpen,setNotificationsOpen]=useState(false)
  useEffect(()=>{let active=true;async function load(){const values=await Promise.allSettled([logApi.list({limit:1}),alertApi.security({status:'ACTIVE',limit:50})]);if(!active)return;const logs=values[0].status==='fulfilled'?values[0].value.total||0:0;const alerts=values[1].status==='fulfilled'?values[1].value.data||[]:[];setCounts({threats:logs,critical:alerts.filter(x=>['HIGH','CRITICAL'].includes(x.severity)).length})}load();const timer=setInterval(load,15000);return()=>{active=false;clearInterval(timer)}},[])
  useEffect(()=>{let active=true;async function load(){try{const data=await notificationApi.list({limit:20});if(active){setNotifications(data.data||[]);setUnread(data.unread_count||0)}}catch{}}load();const timer=setInterval(load,10000);return()=>{active=false;clearInterval(timer)}},[])
  async function markRead(item){if(item.is_read)return;await notificationApi.markRead(item.id);setNotifications(rows=>rows.map(row=>row.id===item.id?{...row,is_read:true}:row));setUnread(value=>Math.max(0,value-1))}
  return (
    <header className="navbar">
      <button className="icon-button mobile-menu" onClick={onMenu} aria-label="Open navigation"><Menu size={21} /></button>
      <div className="search-box">
        <Search size={18} />
        <input aria-label="Search security data" placeholder="Search threats, IPs, assets…" />
        <kbd>⌘ K</kbd>
      </div>
      <div className="navbar-actions">
        <span className="top-counter"><small>Threat events</small><strong>{counts.threats}</strong></span>
        <span className="top-counter critical"><small>Critical</small><strong>{counts.critical}</strong></span>
        <span className="live-indicator"><i /> Live monitoring</span>
        <div className="notification-center"><button className="icon-button notification-button" onClick={()=>setNotificationsOpen(value=>!value)} aria-label={`${unread} unread notifications`}><Bell size={19} />{unread>0&&<b>{unread>99?'99+':unread}</b>}</button>{notificationsOpen&&<div className="notification-dropdown"><div className="notification-dropdown-head"><div><span className="eyebrow">SOC event stream</span><strong>Notifications</strong></div><i>{unread} unread</i></div><div className="notification-scroll">{notifications.length?notifications.map(item=><button className={`notification-item ${item.is_read?'read':''}`} onClick={()=>markRead(item)} key={item.id}><span className={`notification-severity severity-${item.severity.toLowerCase()}`}/><div><strong>{item.title}</strong><p>{item.message}</p><small>{item.related_user&&`User: ${item.related_user} · `}{new Date(item.created_at).toLocaleString()}</small></div>{!item.is_read&&<Check size={13}/>}</button>):<div className="notification-empty">No security notifications</div>}</div></div>}</div>
        <div className="analyst-profile">
          <div className="avatar"><ShieldCheck size={19} /></div>
          <div><strong>{user?.username || 'SOC Analyst'}</strong><small>{user?.role || 'Analyst'}</small></div>
        </div>
        <button className="icon-button" onClick={onLogout} aria-label="Sign out" title="Sign out"><LogOut size={17}/></button>
      </div>
    </header>
  )
}
