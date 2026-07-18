import { useEffect, useState } from 'react'
import { Download, FileBarChart, FileText, ShieldCheck } from 'lucide-react'
import { reportsApi, unwrapList } from '../api/api'
import { PageHeader } from './Threats'

export default function Reports() {
  const [reports, setReports] = useState([])
  useEffect(() => { reportsApi.list().then(data => setReports(unwrapList(data, ['reports']))).catch(() => {}) }, [])
  const fallback = [{ title: 'Executive Security Summary', type: 'Executive', icon: FileBarChart }, { title: 'Threat Intelligence Digest', type: 'Intelligence', icon: ShieldCheck }, { title: 'Incident Response Review', type: 'Operations', icon: FileText }]
  const rows = reports.length ? reports : fallback
  return <div className="page"><PageHeader eyebrow="Security analytics" title="Reports" text="Cross-phase reporting for analysts, leadership, and compliance teams." /><section className="report-grid">{rows.map((report, i) => { const Icon = report.icon || FileText; return <article className="panel report-card" key={report.id || i}><div className="report-icon"><Icon /></div><span>{report.type || report.report_type || 'Security report'}</span><h2>{report.title || report.name}</h2><p>{report.description || 'Consolidated findings from the central threat intelligence pipeline.'}</p><button className="button secondary" disabled={!report.download_url}><Download size={16}/>Generate report</button></article> })}</section></div>
}
