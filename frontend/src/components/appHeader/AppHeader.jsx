import React, { useState, useRef, useEffect } from 'react';
import styles from './AppHeader.module.css';

const SearchIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="11" cy="11" r="8" />
    <line x1="21" y1="21" x2="16.65" y2="16.65" />
  </svg>
);

const BellIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
    <path d="M13.73 21a2 2 0 0 1-3.46 0" />
  </svg>
);

const UserIcon = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
    <circle cx="12" cy="7" r="4" />
  </svg>
);

const ProfileIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
    <circle cx="12" cy="7" r="4" />
  </svg>
);

const LogoutIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
    <polyline points="16 17 21 12 16 7" />
    <line x1="21" y1="12" x2="9" y2="12" />
  </svg>
);

const CloseIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="18" y1="6" x2="6" y2="18" />
    <line x1="6" y1="6" x2="18" y2="18" />
  </svg>
);

const EditIcon = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
  </svg>
);

const AppHeader = ({ title, onLogout }) => {
  const [showDropdown, setShowDropdown] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleAvatarClick = () => {
    setShowDropdown(!showDropdown);
  };

  const handleProfileClick = () => {
    setShowDropdown(false);
    setShowProfile(true);
  };

  const handleCloseProfile = () => {
    setShowProfile(false);
  };

  return (
    <header className={styles.header}>
      <h1 className={styles.title}>{title}</h1>
      <div className={styles.actions}>
        <div className={styles.searchBox}>
          <input className={styles.searchInput} type="text" placeholder="Pesquisar inputs..." />
          <SearchIcon />
        </div>
        <button className={styles.notificationBtn}>
          <BellIcon />
        </button>
        <div className={styles.avatarWrapper} ref={dropdownRef}>
          <div className={styles.avatar} onClick={handleAvatarClick}>
            <UserIcon />
          </div>
          {showDropdown && (
            <div className={styles.dropdown}>
              <div className={styles.dropdownHeader}>
                <span className={styles.dropdownTitle}>Minha Conta</span>
              </div>
              <div className={styles.dropdownDivider} />
              <button className={styles.dropdownItem} onClick={handleProfileClick}>
                <ProfileIcon />
                Meu perfil
              </button>
              <button className={styles.dropdownItem} onClick={onLogout}>
                <LogoutIcon />
                Sair
              </button>
            </div>
          )}
        </div>
      </div>

      {showProfile && (
        <div className={styles.modalOverlay} onClick={handleCloseProfile}>
          <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
            <div className={styles.modalHeader}>
              <h2 className={styles.modalTitle}>Meu Perfil</h2>
              <button className={styles.closeBtn} onClick={handleCloseProfile}>
                <CloseIcon />
              </button>
            </div>
            
            <div className={styles.modalContent}>
              <div className={styles.profileSection}>
                <div className={styles.profileAvatar}>
                  <UserIcon />
                </div>
                <button className={styles.editAvatarBtn}>
                  <EditIcon /> Alterar foto
                </button>
              </div>

              <div className={styles.formGrid}>
                <div className={styles.field}>
                  <label className={styles.label}>Nome completo</label>
                  <input type="text" className={styles.input} defaultValue="Eduardo Silva" />
                </div>
                <div className={styles.field}>
                  <label className={styles.label}>Email</label>
                  <input type="email" className={styles.input} defaultValue="eduardo@email.com" />
                </div>
                <div className={styles.field}>
                  <label className={styles.label}>Telefone</label>
                  <input type="tel" className={styles.input} defaultValue="+55 13 99999-9999" />
                </div>
                <div className={styles.field}>
                  <label className={styles.label}>Cargo</label>
                  <input type="text" className={styles.input} defaultValue="Administrador" />
                </div>
                <div className={styles.fieldFull}>
                  <label className={styles.label}>Empresa</label>
                  <input type="text" className={styles.input} defaultValue="Imobiliária ABC" />
                </div>
              </div>

              <div className={styles.passwordSection}>
                <h3 className={styles.sectionTitle}>Alterar Senha</h3>
                <div className={styles.formGrid}>
                  <div className={styles.field}>
                    <label className={styles.label}>Senha atual</label>
                    <input type="password" className={styles.input} placeholder="••••••••" />
                  </div>
                  <div className={styles.field}>
                    <label className={styles.label}>Nova senha</label>
                    <input type="password" className={styles.input} placeholder="••••••••" />
                  </div>
                </div>
              </div>
            </div>

            <div className={styles.modalFooter}>
              <button className={styles.cancelBtn} onClick={handleCloseProfile}>Cancelar</button>
              <button className={styles.saveBtn}>Salvar Alterações</button>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};

export default AppHeader;
