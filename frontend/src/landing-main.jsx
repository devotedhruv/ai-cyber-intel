import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import LandingApp from '../../landing-page/src/App'
import '../../landing-page/src/styles/global.css'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <LandingApp />
  </StrictMode>,
)
