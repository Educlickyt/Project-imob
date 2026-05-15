import { useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import './App.css'

import LandingPage from './pages/LandingPage'
import Dashboard from './pages/Dashboard'
import LoginModal from './components/loginModal/LoginModal'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleOpenLogin = () => {
    setShowLoginModal(true);
  };

  const handleCloseLogin = () => {
    setShowLoginModal(false);
  };

  const handleLoginSuccess = () => {
    setShowLoginModal(false);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_type');
    setIsAuthenticated(false);
  };

  return (
    <BrowserRouter>
      <LoginModal 
        isOpen={showLoginModal} 
        onClose={handleCloseLogin} 
        onLoginSuccess={handleLoginSuccess} 
      />
      
      <Routes>
        {isAuthenticated ? (
          <>
            <Route path="/dashboard" element={<Dashboard onLogout={handleLogout} />} />
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </>
        ) : (
          <>
            <Route path="/" element={<LandingPage onLoginClick={handleOpenLogin} />} />
            <Route path="*" element={<LandingPage onLoginClick={handleOpenLogin} />} />
          </>
        )}
      </Routes>
    </BrowserRouter>
  )
}

export default App;