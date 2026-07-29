import { useState } from 'react';
import styles from './contactForm.module.css';
import publicApi from '../../services/publicApi';

export default function ContactForm({ propertyId, slug }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: 'Olá! Tenho interesse neste imóvel.'
  });
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true)
    try{
      await publicApi.post(`/${slug}/contact`, {
        name: formData.name,
        email: formData.email,
        phone: formData.phone,
        message: formData.message,
        property_id: propertyId
      });
      setSubmitted(true);
    }catch(err){
      setError(err.response?.data?.detail || "Erro ao enviar formulário. Tente novamente.");
    }
    finally{
      setLoading(false)
    }
  };

  if (submitted) {
    return (
      <div className={styles.success}>
        Mensagem enviada com sucesso!
      </div>
    );
  }

  if(error){
    return <div className={styles.error}>{error}</div>;
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <div className={styles.group}>
        <label htmlFor="name">Nome</label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
      </div>
      <div className={styles.group}>
        <label htmlFor="email">E-mail</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </div>
      <div className={styles.group}>
        <label htmlFor="phone">Telefone</label>
        <input
          type="tel"
          id="phone"
          name="phone"
          value={formData.phone}
          onChange={handleChange}
          required
        />
      </div>
      <div className={styles.group}>
        <label htmlFor="message">Mensagem</label>
        <textarea
          id="message"
          name="message"
          value={formData.message}
          onChange={handleChange}
          rows={4}
        />
      </div>
      <button type="submit" className={styles.submit}>
        Enviar mensagem
      </button>
    </form>
  );
}
