import React from 'react';

import Menu from '../components/menu/Menu';
import PropertyMediaUploader from '../components/propertyMediaUploader/PropertyMediaUploader'

const Dashboard = ({ onLogout }) => {
  return (
    <div>
      <Menu/>
      <main style={{marginLeft:'80px', width: 'calc(100% - 80px)'}}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px 24px', borderBottom: '1px solid #eee' }}>
          <h1 style={{ margin: 0, fontSize: '1.25rem' }}>Painel de Controle</h1>
          <button
            onClick={onLogout}
            style={{
              padding: '8px 16px',
              backgroundColor: '#BD0D24',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer'
            }}
          >
            Sair
          </button>
        </div>
        <PropertyMediaUploader />
      </main>
    </div>
  );
};

export default Dashboard;