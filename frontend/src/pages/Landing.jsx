import { useCallback } from 'react'
import { useNavigate } from 'react-router-dom'

const LEGACY_DASHBOARD_URL = 'http://localhost:5173'

export default function Landing() {
  const navigate = useNavigate()
  const connectDashboardLinks = useCallback((event) => {
    const document = event.currentTarget.contentDocument
    if (!document) return

    document.querySelectorAll(`a[href="${LEGACY_DASHBOARD_URL}"]`).forEach((link) => {
      link.removeAttribute('target')
      link.addEventListener('click', (clickEvent) => {
        clickEvent.preventDefault()
        navigate('/login')
      }, { once: true })
    })
  }, [navigate])

  return <iframe className="landing-frame" src="/landing.html" title="AI Cyber Threat Intelligence System" onLoad={connectDashboardLinks} />
}
