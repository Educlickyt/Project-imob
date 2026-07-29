import { useState } from 'react';
import styles from './contactForm.module.css';

export default function ContactForm({ propertyId }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: 'Olá! Tenho interesse neste imóvel.'
  });
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: enviar para /v1/{slug}/contact (Etapa 4)
    setSubmitted(true);
  };

  if (submitted) {
    return (
      <div className={styles.success}>
        Mensagem enviada com sucesso!
      </div>
    );
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
