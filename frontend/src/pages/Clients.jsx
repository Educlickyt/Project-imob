import React from 'react';

import Menu from '../components/menu/Menu';
import AppHeader from '../components/appHeader/AppHeader';
import styles from './Clients.module.css';

const PlusIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
    <circle cx="8.5" cy="7" r="4" />
    <line x1="20" y1="8" x2="20" y2="14" />
    <line x1="23" y1="11" x2="17" y2="11" />
  </svg>
);

const tableColumns = ['Nome', 'Email', 'Telefone', 'Documento', 'Corretor', 'Status'];

const tableRows = [
  { id: 1 },
  { id: 2 },
  { id: 3 },
  { id: 4 },
  { id: 5 },
  { id: 6 },
  { id: 7 },
  { id: 8 },
  { id: 9 },
  { id: 10 },
];

const Clients = ({ onLogout }) => {
  return (
    <div>
      <Menu />
      <main style={{ marginLeft: '80px', width: 'calc(100% - 80px)', height: '100vh', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        <AppHeader title="Gerenciamento de Clientes" onLogout={onLogout} />

        <div className={styles.page}>

          {/* ========== STATS ROW ========== */}
          <div className={styles.statsRow}>

            <div className={styles.statCard}>
              <p className={styles.statTitle}>Novos Clientes Nesse Mês</p>
              <p className={styles.statValue}>12</p>
              <p className={styles.statSubtext}>+ 8% comparado aos últimos 30 dias</p>
            </div>

            <div className={styles.statCard}>
              <p className={styles.statTitle}>Seus Clientes</p>
              <p className={styles.statValue}>72</p>
              <p className={styles.statSubtext}>+ 7 cadastrados nesse mês</p>
            </div>

            <div className={styles.statCardWide}>
              <p className={styles.statTitle}>Clientes Cadastrados no Sistema</p>
              <div className={styles.chartPlaceholder}>
                <svg viewBox="0 0 400 100" className={styles.miniChart}>
                  <polyline
                    fill="none"
                    stroke="var(--text-h)"
                    strokeWidth="2"
                    points="0,80 60,70 120,40 180,45 240,30 300,25 360,20 400,18"
                  />
                </svg>
              </div>
            </div>
          </div>

          {/* ========== FILTERS ========== */}
          <div className={styles.filtersRow}>
            <input className={styles.searchInput} type="text" placeholder="Buscar cliente por nome" />
            <input className={styles.searchInput} type="text" placeholder="exemplo@gmail.com" />
            <input className={styles.searchInput} type="text" placeholder="Documento" />
            <select className={styles.select}>
              <option>Corretor</option>
              <option>Corretor 1</option>
              <option>Corretor 2</option>
            </select>
            <select className={styles.select}>
              <option>Status</option>
              <option>Ativo</option>
              <option>Inativo</option>
            </select>
            <button className={styles.addBtn}>
              <PlusIcon /> Cadastrar Cliente
            </button>
          </div>

          {/* ========== TABLE ========== */}
          <div className={styles.tableWrapper}>
            <table className={styles.table}>
              <thead>
                <tr>
                  {tableColumns.map((col) => (
                    <th key={col} className={styles.th}>{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {tableRows.map((row) => (
                  <tr key={row.id} className={styles.tr}>
                    {tableColumns.map((col) => (
                      <td key={col} className={styles.td}></td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

        </div>
      </main>
    </div>
  );
};

export default Clients;
