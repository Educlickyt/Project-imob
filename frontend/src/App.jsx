import { useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import './App.css'

import LandingPage from './pages/LandingPage'
import Dashboard from './pages/Dashboard'
import Properties from './pages/Properties'
import Leads from './pages/Leads'
import Clients from './pages/Clients'
import PropertyOwners from './pages/PropertyOwners'
import Collaborators from './pages/Collaborators'
import Settings from './pages/Settings'
import ShowcaseList from './pages/ShowcaseList'
import ShowcaseDetail from './pages/ShowcaseDetail'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      setIsAuthenticated(true);
    }
    setIsLoading(false);
  }, []);

  const handleAuthSuccess = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_type');

    // deletar refresh_token !

    setIsAuthenticated(false);
  };

  if (isLoading) {
    return null;
  }

  return (
    <BrowserRouter>
      <Routes>
        {/* Rotas da vitrine - sempre acessíveis */}
        <Route path="/v/:slug" element={<ShowcaseList />} />
        <Route path="/v/:slug/:id" element={<ShowcaseDetail />} />

        {isAuthenticated ? (
          <>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard onLogout={handleLogout} />} />
            <Route path="/properties" element={<Properties onLogout={handleLogout} />} />
            <Route path="/leads" element={<Leads onLogout={handleLogout} />} />
            <Route path="/clients" element={<Clients onLogout={handleLogout} />} />
            <Route path="/property-owners" element={<PropertyOwners onLogout={handleLogout} />} />
            <Route path="/tenant-users" element={<Collaborators onLogout={handleLogout} />} />
            <Route path="/settings" element={<Settings onLogout={handleLogout} />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </>
        ) : (
          <>
            <Route path="/" element={<LandingPage onAuthSuccess={handleAuthSuccess} />} />
            <Route path="/dashboard" element={<Navigate to="/" replace />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </>
        )}
      </Routes>
    </BrowserRouter>
  )
}

export default App;