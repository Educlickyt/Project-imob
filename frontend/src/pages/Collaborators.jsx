import React, { useState } from 'react';

import Menu from '../components/menu/Menu';
import AppHeader from '../components/appHeader/AppHeader';
import styles from './Collaborators.module.css';

const PlusIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
    <circle cx="8.5" cy="7" r="4" />
    <line x1="20" y1="8" x2="20" y2="14" />
    <line x1="23" y1="11" x2="17" y2="11" />
  </svg>
);

const ChatIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
  </svg>
);

const LockIcon = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
    <path d="M7 11V7a5 5 0 0 1 10 0v4" />
  </svg>
);

const EditIcon = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
  </svg>
);

const TrashIcon = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="3 6 5 6 21 6" />
    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
  </svg>
);

const collaboratorsData = [
  { id: 1, name: 'Rodolfo Silva dos Santos', role: 'Corretor', email: 'rodolfossantos5421@gmail.com', phone: '+55 13 9876 - 5421', lastAccess: '25/10/2025 - 12:52:02' },
  { id: 2, name: 'Rodolfo Silva dos Santos', role: 'Corretor', email: 'rodolfossantos5421@gmail.com', phone: '+55 13 9876 - 5421', lastAccess: '25/10/2025 - 12:52:02' },
  { id: 3, name: 'Rodolfo Silva dos Santos', role: 'Corretor', email: 'rodolfossantos5421@gmail.com', phone: '+55 13 9876 - 5421', lastAccess: '25/10/2025 - 12:52:02' },
  { id: 4, name: 'Rodolfo Silva dos Santos', role: 'Corretor', email: 'rodolfossantos5421@gmail.com', phone: '+55 13 9876 - 5421', lastAccess: '25/10/2025 - 12:52:02' },
  { id: 5, name: 'Rodolfo Silva dos Santos', role: 'Corretor', email: 'rodolfossantos5421@gmail.com', phone: '+55 13 9876 - 5421', lastAccess: '25/10/2025 - 12:52:02' },
  { id: 6, name: 'Rodolfo Silva dos Santos', role: 'Corretor', email: 'rodolfossantos5421@gmail.com', phone: '+55 13 9876 - 5421', lastAccess: '25/10/2025 - 12:52:02' },
  { id: 7, name: 'Rodolfo Silva dos Santos', role: 'Corretor', email: 'rodolfossantos5421@gmail.com', phone: '+55 13 9876 - 5421', lastAccess: '25/10/2025 - 12:52:02' },
  { id: 8, name: 'Rodolfo Silva dos Santos', role: 'Corretor', email: 'rodolfossantos5421@gmail.com', phone: '+55 13 9876 - 5421', lastAccess: '25/10/2025 - 12:52:02' },
];

const Collaborators = ({ onLogout }) => {
  const [selectedIds, setSelectedIds] = useState([]);

  const toggleSelect = (id) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]
    );
  };

  const toggleSelectAll = () => {
    if (selectedIds.length === collaboratorsData.length) {
      setSelectedIds([]);
    } else {
      setSelectedIds(collaboratorsData.map((c) => c.id));
    }
  };

  const handleRowClick = (collab) => {
    if (selectedIds.length > 0) {
      toggleSelect(collab.id);
    } else {
      // TODO: abrir popup do colaborador
      console.log('Abrir popup do colaborador:', collab);
    }
  };

  const isAllSelected = selectedIds.length === collaboratorsData.length && collaboratorsData.length > 0;

  return (
    <div>
      <Menu />
      <main style={{ marginLeft: '80px', width: 'calc(100% - 80px)', height: '100vh', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        <AppHeader title="Gerenciamento de Colaboradores" onLogout={onLogout} />

        <div className={styles.page}>

          {/* ========== STATS ROW ========== */}
          <div className={styles.statsRow}>
            <div className={styles.statCard}>
              <p className={styles.statTitle}>Total de Colaboradores</p>
              <p className={styles.statValue}>24</p>
              <p className={styles.statSubtext}>cadastrados no sistema</p>
            </div>
            <div className={styles.statCard}>
              <p className={styles.statTitle}>Colaboradores Ativos</p>
              <p className={styles.statValue}>21</p>
              <p className={styles.statSubtext}>87% do total</p>
            </div>
            <div className={styles.statCard}>
              <p className={styles.statTitle}>Novos esse Mês</p>
              <p className={styles.statValue}>3</p>
              <p className={styles.statSubtext}>+2 comparado ao mês anterior</p>
            </div>
          </div>

          {/* ========== FILTERS ========== */}
          <div className={styles.filtersRow}>
            <input className={styles.searchInput} type="text" placeholder="Buscar colaborador..." />
            <select className={styles.select}>
              <option>Função</option>
              <option>Corretor</option>
              <option>Administrador</option>
              <option>Assistente</option>
            </select>
            <select className={styles.select}>
              <option>Status</option>
              <option>Ativo</option>
              <option>Inativo</option>
            </select>
            <div className={styles.filtersRight}>
              <button className={styles.iconBtn}>
                <ChatIcon />
              </button>
              <button className={styles.addBtn}>
                <PlusIcon /> Cadastrar Colaborador
              </button>
            </div>
          </div>

          {/* ========== COLLABORATORS LIST ========== */}
          <div className={styles.listWrapper}>
            {/* Header */}
            <div className={styles.listHeader}>
              <span className={styles.colName}>Nome completo</span>
              <span className={styles.colRole}>Função</span>
              <span className={styles.colEmail}>Email</span>
              <span className={styles.colPhone}>Numero</span>
              <span className={styles.colAccess}>Ultimo Acesso</span>
              <div className={styles.colActions}>
                <input
                  type="checkbox"
                  checked={isAllSelected}
                  onChange={toggleSelectAll}
                  className={styles.checkbox}
                />
                <span>Ações</span>
              </div>
            </div>

            {/* Rows */}
            {collaboratorsData.map((collab) => (
              <div
                key={collab.id}
                className={`${styles.listRow} ${selectedIds.includes(collab.id) ? styles.listRowSelected : ''}`}
                onClick={() => handleRowClick(collab)}
              >
                <div className={styles.colName}>
                  <div className={styles.avatar}></div>
                  <span>{collab.name}</span>
                </div>
                <span className={styles.colRole}>{collab.role}</span>
                <span className={styles.colEmail}>{collab.email}</span>
                <span className={styles.colPhone}>{collab.phone}</span>
                <span className={styles.colAccess}>{collab.lastAccess}</span>
                <div className={styles.colActions}>
                  <input
                    type="checkbox"
                    checked={selectedIds.includes(collab.id)}
                    onChange={() => toggleSelect(collab.id)}
                    onClick={(e) => e.stopPropagation()}
                    className={styles.checkbox}
                  />
                  <button className={styles.actionBtn}><LockIcon /></button>
                  <button className={styles.actionBtn}><EditIcon /></button>
                  <button className={styles.actionBtn}><TrashIcon /></button>
                </div>
              </div>
            ))}
          </div>

        </div>
      </main>
    </div>
  );
};

export default Collaborators;
