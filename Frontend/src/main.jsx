import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import MyProvider from './context/MyContext'
import "rsuite/dist/rsuite.css";

createRoot(document.getElementById('root')).render(
  // <StrictMode>
  <MyProvider>

    <App />
  </MyProvider>
  // </StrictMode>,
)
