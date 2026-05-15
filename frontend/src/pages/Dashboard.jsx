import React from 'react';

const Dashboard = ({ onLogout }) => {
  return (
    <div style={{ padding: '40px', textAlign: 'center' }}>
      <h1>Dashboard</h1>
      <p>Bem-vindo ao seu painel de controle!</p>
      <button 
        onClick={onLogout}
        style={{
          padding: '10px 20px',
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
  );
};

export default Dashboard;