import React, { useState } from 'react'
import Header from '../components/header/Header'
import HeroBanner from '../components/heroBanner/HeroBanner'
import LoginModal from '../components/loginModal/LoginModal'
import RegisterModal from '../components/loginModal/RegisterModal'

const LandingPage = ({ onAuthSuccess }) => {
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showRegisterModal, setShowRegisterModal] = useState(false);

  const handleOpenLogin = () => {
    setShowLoginModal(true);
    setShowRegisterModal(false);
  };

  const handleOpenRegister = () => {
    setShowRegisterModal(true);
    setShowLoginModal(false);
  };

  const handleCloseLogin = () => {
    setShowLoginModal(false);
  };

  const handleCloseRegister = () => {
    setShowRegisterModal(false);
  };

  const handleLoginSuccess = () => {
    setShowLoginModal(false);
    setShowRegisterModal(false);
    if (onAuthSuccess) {
      onAuthSuccess();
    }
  };

  return (
    <>
      <Header onLoginClick={handleOpenLogin} />
      <HeroBanner />
      
      <LoginModal 
        isOpen={showLoginModal} 
        onClose={handleCloseLogin} 
        onLoginSuccess={handleLoginSuccess}
        onSwitchToRegister={handleOpenRegister}
      />
      
      <RegisterModal
        isOpen={showRegisterModal}
        onClose={handleCloseRegister}
        onSwitchToLogin={handleOpenLogin}
        onRegisterSuccess={handleLoginSuccess}
      />
    </>
  )
}

export default LandingPage;