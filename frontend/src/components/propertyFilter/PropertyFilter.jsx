import React from 'react';
import styles from './PropertyFilter.module.css';

const SearchIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="11" cy="11" r="8" />
    <line x1="21" y1="21" x2="16.65" y2="16.65" />
  </svg>
);

const FilterIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" />
  </svg>
);

const NumberButtons = ({ label, selected, onSelect }) => (
  <div className={styles.filterGroup}>
    <label className={styles.filterLabel}>{label}</label>
    <div className={styles.numberButtons}>
      {[1, 2, 3, 4, '5+'].map((num) => (
        <button
          key={num}
          className={`${styles.numberBtn} ${selected === num ? styles.numberBtnActive : ''}`}
          onClick={() => onSelect(num)}
        >
          {num}
        </button>
      ))}
    </div>
  </div>
);

const PropertyFilter = () => {
  return (
    <div className={styles.filterCard}>
      <div className={styles.filterHeader}>
        <h2 className={styles.filterTitle}>Filtrar listagem dos imóveis</h2>
        <div className={styles.filterActions}>
          <button className={styles.searchBtn}>
            <SearchIcon /> Buscar
          </button>
          <button className={styles.clearBtn}>
            <FilterIcon /> Limpar Filtros
          </button>
        </div>
      </div>

      <div className={styles.filterRows}>
        {/* Linha 1 */}
        <div className={styles.filterRow}>
          <div className={styles.filterGroup}>
            <label className={styles.filterLabel}>Tipo</label>
            <select className={styles.select}>
              <option>Apartamento</option>
              <option>Casa</option>
              <option>Terreno</option>
              <option>Comercial</option>
            </select>
          </div>

          <div className={styles.filterGroup}>
            <label className={styles.filterLabel}>Cidades</label>
            <select className={styles.select}>
              <option>Selecione...</option>
            </select>
          </div>

          <div className={styles.filterGroup}>
            <label className={styles.filterLabel}>Bairros</label>
            <select className={styles.select}>
              <option>Selecione...</option>
            </select>
          </div>

          <div className={styles.filterGroup}>
            <label className={styles.filterLabel}>Área</label>
            <div className={styles.inputPair}>
              <input className={styles.input} type="text" placeholder="De: M²" />
              <input className={styles.input} type="text" placeholder="Até: M²" />
            </div>
          </div>

          <div className={styles.filterGroup}>
            <label className={styles.filterLabel}>Corretor</label>
            <select className={styles.select}>
              <option>Selecione...</option>
            </select>
          </div>
        </div>

        {/* Linha 2 */}
        <div className={styles.filterRow}>
          <div className={styles.filterGroup}>
            <label className={styles.filterLabel}>Locação</label>
            <div className={styles.checkboxRow}>
              <input type="checkbox" className={styles.checkbox} />
              <div className={styles.inputPair}>
                <input className={styles.input} type="text" placeholder="De: R$" />
                <input className={styles.input} type="text" placeholder="Até: R$" />
              </div>
            </div>
          </div>

          <div className={styles.filterGroup}>
            <label className={styles.filterLabel}>Venda</label>
            <div className={styles.checkboxRow}>
              <input type="checkbox" className={styles.checkbox} />
              <div className={styles.inputPair}>
                <input className={styles.input} type="text" placeholder="De: R$" />
                <input className={styles.input} type="text" placeholder="Até: R$" />
              </div>
            </div>
          </div>

          <NumberButtons label="Dormitórios" />
          <NumberButtons label="Vagas" />
          <NumberButtons label="Banheiros" />

          <div className={styles.filterGroup}>
            <label className={styles.filterLabel}>Status</label>
            <select className={styles.select}>
              <option>Ativo</option>
              <option>Inativo</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PropertyFilter;
