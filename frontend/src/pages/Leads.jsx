import React from 'react';

import Menu from '../components/menu/Menu';
import AppHeader from '../components/appHeader/AppHeader';
import styles from './Leads.module.css';

const sourceData = [
  { label: 'Vitrine', value: 38 },
  { label: 'OLX', value: 52 },
  { label: '(Portal de anúncio)', value: 10 },
];

const maxSource = Math.max(...sourceData.map((d) => d.value));

const tableColumns = ['Nome', 'Email', 'Telefone', 'Imóvel', 'Origem', 'Status', 'Data'];

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

const Leads = ({ onLogout }) => {
  return (
    <div>
      <Menu />
      <main style={{ marginLeft: '80px', width: 'calc(100% - 80px)', height: '100vh', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        <AppHeader title="Gerenciamento de Leads" onLogout={onLogout} />

        <div className={styles.page}>

          {/* ========== STATS ROW ========== */}
          <div className={styles.statsRow}>

            <div className={styles.statCard}>
              <p className={styles.statTitle}>Leads Aguardando Resposta</p>
              <p className={styles.statValue}>12</p>
              <p className={styles.statSubtext}>+ 3 hoje</p>
            </div>

            <div className={styles.statCard}>
              <p className={styles.statTitle}>Novos Leads Nesse Mês</p>
              <p className={styles.statValue}>54</p>
              <p className={styles.statSubtext}>+ 15% comparado aos últimos 30 dias</p>
            </div>

            <div className={styles.statCard}>
              <p className={styles.statTitle}>Leads Convertidos</p>
              <p className={styles.statValue}>32</p>
              <p className={styles.statSubtext}>47% dos leads se tornaram clientes</p>
            </div>

            <div className={styles.statCard}>
              <p className={styles.statTitle}>Fonte dos Leads</p>
              <div className={styles.sourceChart}>
                {sourceData.map((item) => (
                  <div key={item.label} className={styles.sourceRow}>
                    <span className={styles.sourceLabel}>{item.label}</span>
                    <div className={styles.sourceTrack}>
                      <div
                        className={styles.sourceFill}
                        style={{ width: `${(item.value / maxSource) * 100}%` }}
                      />
                    </div>
                    <span className={styles.sourceValue}>{item.value}%</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* ========== FILTERS ========== */}
          <div className={styles.filtersRow}>
            <input className={styles.searchInput} type="text" placeholder="Pesquisar leads..." />
            <select className={styles.statusSelect}>
              <option>Status</option>
              <option>Novo</option>
              <option>Em contato</option>
              <option>Convertido</option>
              <option>Inativo</option>
            </select>
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

export default Leads;
