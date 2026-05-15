import React, { useState } from 'react';
import api from '../../services/api';
import styles from './LoginModal.module.css';

const RegisterModal = ({ isOpen, onClose, onSwitchToLogin, onRegisterSuccess }) => {
  if (!isOpen) return null;

  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    phone: '',
    tenant_name: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await api.post('/auth/register', formData);
      
      const loginResponse = await api.post('/auth/login', {
        email: formData.email,
        password: formData.password
      });

      localStorage.setItem('access_token', loginResponse.data.access_token);
      localStorage.setItem('token_type', loginResponse.data.token_type);

      setSuccess('Cadastro realizado com sucesso!');
      
      setTimeout(() => {
        if (onRegisterSuccess) {
          onRegisterSuccess();
        }
      }, 1000);
    } catch (err) {
      setLoading(false);
      if (err.response && err.response.data) {
        const detail = err.response.data.detail;
        if (Array.isArray(detail)) {
          setError(detail.map(d => d.msg).join(', '));
        } else {
          setError(detail || 'Erro ao fazer cadastro');
        }
      } else {
        setError('Erro de conexão. Verifique se o backend está rodando.');
      }
    }
  };

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modalContent} onClick={e => e.stopPropagation()}>
        <div className={styles.modalHeader}>
          <h2>Criar conta</h2>
          <button className={styles.modalClose} onClick={onClose}>
            ×
          </button>
        </div>
        
        {error && <div className={styles.errorMessage}>{error}</div>}
        {success && <div className={styles.successMessage}>{success}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className={styles.formGroup}>
            <label htmlFor="name">
              <span>Nome:</span>
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Seu nome completo"
              required
              disabled={loading}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="email">
              <span>Email:</span>
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Seu email"
              required
              disabled={loading}
            />
          </div>
          
          <div className={styles.formGroup}>
            <label htmlFor="phone">
              <span>Telefone:</span>
            </label>
            <input
              type="tel"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="Seu telefone"
              required
              disabled={loading}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="tenant_name">
              <span>Nome da empresa/imóvel:</span>
            </label>
            <input
              type="text"
              id="tenant_name"
              name="tenant_name"
              value={formData.tenant_name}
              onChange={handleChange}
              placeholder="Nome da sua empresa ou imóvel"
              required
              disabled={loading}
            />
          </div>
          
          <div className={styles.formGroup}>
            <label htmlFor="password">
              <span>Senha:</span>
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Mínimo 8 caracteres"
              required
              minLength="8"
              disabled={loading}
            />
          </div>
          
          <button 
            type="submit" 
            className={styles.loginButton}
            disabled={loading}
          >
            {loading ? 'Cadastrando...' : 'Cadastrar'}
          </button>

          <div className={styles.switchMode}>
            <span>Já tem conta? </span>
            <button type="button" onClick={onSwitchToLogin} className={styles.switchButton}>
              Fazer login
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RegisterModal;