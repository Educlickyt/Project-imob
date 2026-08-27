import React, { useState } from 'react';
import { Link } from 'react-router-dom';

import Menu from '../components/menu/Menu';
import AppHeader from '../components/appHeader/AppHeader';
import PropertyFilter from '../components/propertyFilter/PropertyFilter';
import Pagination from '../components/pagination/Pagination';
import styles from './Properties.module.css';

const GridIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="3" width="7" height="7" />
    <rect x="14" y="3" width="7" height="7" />
    <rect x="3" y="14" width="7" height="7" />
    <rect x="14" y="14" width="7" height="7" />
  </svg>
);

const ListIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="8" y1="6" x2="21" y2="6" />
    <line x1="8" y1="12" x2="21" y2="12" />
    <line x1="8" y1="18" x2="21" y2="18" />
    <line x1="3" y1="6" x2="3.01" y2="6" />
    <line x1="3" y1="12" x2="3.01" y2="12" />
    <line x1="3" y1="18" x2="3.01" y2="18" />
  </svg>
);

const PlusIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="12" y1="5" x2="12" y2="19" />
    <line x1="5" y1="12" x2="19" y2="12" />
  </svg>
);

const propertiesData = [
  { id: 1, title: 'Imóvel ponta da praia tararau', address: 'Endereço rua do sabão, bairro do negão', area: 89, bedrooms: 3, bathrooms: 2, garage_spots: 3, image: 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400&h=300&fit=crop' },
  { id: 2, title: 'Imóvel ponta da praia tararau', address: 'Endereço rua do sabão, bairro do negão', area: 89, bedrooms: 3, bathrooms: 2, garage_spots: 3, image: 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400&h=300&fit=crop' },
  { id: 3, title: 'Imóvel ponta da praia tararau', address: 'Endereço rua do sabão, bairro do negão', area: 89, bedrooms: 3, bathrooms: 2, garage_spots: 3, image: 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=400&h=300&fit=crop' },
  { id: 4, title: 'Imóvel ponta da praia tararau', address: 'Endereço rua do sabão, bairro do negão', area: 89, bedrooms: 3, bathrooms: 2, garage_spots: 3, image: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=400&h=300&fit=crop' },
  { id: 5, title: 'Imóvel ponta da praia tararau', address: 'Endereço rua do sabão, bairro do negão', area: 89, bedrooms: 3, bathrooms: 2, garage_spots: 3, image: 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=400&h=300&fit=crop' },
  { id: 6, title: 'Imóvel ponta da praia tararau', address: 'Endereço rua do sabão, bairro do negão', area: 89, bedrooms: 3, bathrooms: 2, garage_spots: 3, image: 'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=400&h=300&fit=crop' },
  { id: 7, title: 'Imóvel ponta da praia tararau', address: 'Endereço rua do sabão, bairro do negão', area: 89, bedrooms: 3, bathrooms: 2, garage_spots: 3, image: 'https://images.unsplash.com/photo-1600573472550-8090b5e0745e?w=400&h=300&fit=crop' },
  { id: 8, title: 'Imóvel ponta da praia tararau', address: 'Endereço rua do sabão, bairro do negão', area: 89, bedrooms: 3, bathrooms: 2, garage_spots: 3, image: 'https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=400&h=300&fit=crop' },
];

const Properties = ({ onLogout }) => {
  const [viewMode, setViewMode] = useState('grid');
  const [currentPage, setCurrentPage] = useState(2);
  const totalPages = 54;

  return (
    <div>
      <Menu />
      <main style={{ marginLeft: '80px', width: 'calc(100% - 80px)' }}>
        <AppHeader title="Gerenciamento dos Imóveis" onLogout={onLogout} />

        <div className={styles.page}>
          <PropertyFilter />

          <div className={styles.resultsBar}>
            <span className={styles.resultsText}>Resultados - pagina {currentPage} / {totalPages}</span>
            <div className={styles.resultsActions}>
              <button
                className={`${styles.viewBtn} ${viewMode === 'grid' ? styles.viewBtnActive : ''}`}
                onClick={() => setViewMode('grid')}
              >
                <GridIcon />
              </button>
              <button
                className={`${styles.viewBtn} ${viewMode === 'list' ? styles.viewBtnActive : ''}`}
                onClick={() => setViewMode('list')}
              >
                <ListIcon />
              </button>
              <button className={styles.addBtn}>
                <PlusIcon /> Cadastrar Imóvel
              </button>
            </div>
          </div>

          <div className={viewMode === 'grid' ? styles.grid : styles.list}>
            {propertiesData.map((prop) => (
              <Link key={prop.id} to="#" className={viewMode === 'grid' ? styles.gridCard : styles.listCard}>
                <div className={viewMode === 'grid' ? styles.gridImage : styles.listImage}>
                  <img src={prop.image} alt={prop.title} />
                </div>
                <div className={viewMode === 'grid' ? styles.gridInfo : styles.listInfo}>
                  <h3 className={styles.cardTitle}>{prop.title}</h3>
                  <p className={styles.cardAddress}>{prop.address}</p>
                  <p className={styles.cardDetails}>{prop.area} m² – {prop.bedrooms} Dormitórios | {prop.bathrooms} Banheiros | {prop.garage_spots} Vagas</p>
                </div>
              </Link>
            ))}
          </div>

          <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={setCurrentPage} />
        </div>
      </main>
    </div>
  );
};

export default Properties;
