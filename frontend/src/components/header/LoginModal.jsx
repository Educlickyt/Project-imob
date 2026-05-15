import React, { useState } from 'react';
import LoginModal from '../loginModal/LoginModal';
import styles from './LoginModal.module.css';

const LoginModal = ({ isOpen, onClose, onLoginSuccess }) => {
  if (!isOpen) return null;

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modalContent} onClick={e => e.stopPropagation()}>
        <div className={styles.modalHeader}>
          <h2>Acesse sua conta</h2>
          <button className={styles.modalClose} onClick={onClose}>
            ×
          </button>
        </div>
        <LoginModal onLoginSuccess={onLoginSuccess} />
      </div>
    </div>
  );
};

export default LoginModal;