import React, { useState } from 'react';

import Menu from '../components/menu/Menu';
import AppHeader from '../components/appHeader/AppHeader';
import Pagination from '../components/pagination/Pagination';
import styles from './PropertyOwners.module.css';

const PlusIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
    <circle cx="8.5" cy="7" r="4" />
    <line x1="20" y1="8" x2="20" y2="14" />
    <line x1="23" y1="11" x2="17" y2="11" />
  </svg>
);

const tableColumns = ['Nome', 'Email', 'Telefone', 'Documento', 'Imóveis', 'Status'];

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

const PropertyOwners = ({ onLogout }) => {
  const [currentPage, setCurrentPage] = useState(2);
  const totalPages = 10;

  return (
    <div>
      <Menu />
      <main style={{ marginLeft: '80px', width: 'calc(100% - 80px)', height: '100vh', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        <AppHeader title="Gerenciamento de Proprietários" onLogout={onLogout} />

        <div className={styles.page}>

          {/* ========== FILTERS ========== */}
          <div className={styles.filtersRow}>
            <input className={styles.searchInput} type="text" placeholder="Buscar proprietário..." />
            <select className={styles.select}>
              <option>Função</option>
              <option>Proprietário</option>
              <option>Administrador</option>
            </select>
            <select className={styles.select}>
              <option>Status</option>
              <option>Ativo</option>
              <option>Inativo</option>
            </select>
            <button className={styles.addBtn}>
              <PlusIcon /> Cadastrar Proprietário
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

          <div className={styles.paginationWrapper}>
            <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={setCurrentPage} />
          </div>

        </div>
      </main>
    </div>
  );
};

export default PropertyOwners;
