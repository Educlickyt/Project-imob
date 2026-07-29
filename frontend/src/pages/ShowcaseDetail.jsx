import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import publicApi from '../services/publicApi';
import ShowcaseLayout from '../components/showcaseLayout/showcaseLayout';
import ContactForm from '../components/contactForm/contactForm';
import styles from './ShowcaseDetail.module.css';

export default function ShowcaseDetail() {
  const { slug, id } = useParams();
  const [info, setInfo] = useState(null);
  const [property, setProperty] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    publicApi.get(`/${slug}/info`)
      .then(res => setInfo(res.data))
      .catch(() => setError('Corretora não encontrada'));
  }, [slug]);

  useEffect(() => {
    if (!info) return;
    publicApi.get(`/${slug}/properties/${id}`)
      .then(res => setProperty(res.data))
      .catch(() => setError('Imóvel não encontrado'))
      .finally(() => setLoading(false));
  }, [slug, id, info]);

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  if (!info || !property) {
    return <div className={styles.loading}>Carregando...</div>;
  }

  let price = 0
  if(property.transaction_type === 'sale'){
    price = property.price_sale;
  }
  else{
    price = property.price_rent;
  }

  const formattedPrice = price
    ? new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(price)
    : 'Consulte';

  const transactionLabel = property.transaction_type === 'sale' ? 'Venda' : 'Aluguel';
  const fullAddress = [property.address, property.district, property.city, property.state].filter(Boolean).join(', ');

  return (
    <ShowcaseLayout info={info}>
      <a href={`/v/${slug}`} className={styles.backLink}>&larr; Voltar</a>

      <div className={styles.detail}>
        <div className={styles.gallery}>
          {property.medias && property.medias.length > 0 ? (
            property.medias.map((media, index) => (
              <img
                key={media.id}
                src={`http://localhost:8000/media/${media.id}`}
                alt={`${property.title} ${index + 1}`}
                className={styles.image}
              />
            ))
          ) : (
            <div className={styles.noImage}>Sem imagens</div>
          )}
        </div>

        <div className={styles.content}>
          <div className={styles.header}>
            <span className={styles.badge}>{transactionLabel}</span>
            <h1 className={styles.title}>{property.title}</h1>
            <p className={styles.price}>{formattedPrice}</p>
          </div>

          <div className={styles.specs}>
            {property.bedrooms != null && (
              <div className={styles.spec}>
                <span className={styles.specValue}>{property.bedrooms}</span>
                <span className={styles.specLabel}>Quartos</span>
              </div>
            )}
            {property.bathrooms != null && (
              <div className={styles.spec}>
                <span className={styles.specValue}>{property.bathrooms}</span>
                <span className={styles.specLabel}>Banheiros</span>
              </div>
            )}
            {property.garage_spots != null && (
              <div className={styles.spec}>
                <span className={styles.specValue}>{property.garage_spots}</span>
                <span className={styles.specLabel}>Vagas</span>
              </div>
            )}
            {property.area != null && (
              <div className={styles.spec}>
                <span className={styles.specValue}>{property.area}m²</span>
                <span className={styles.specLabel}>Área</span>
              </div>
            )}
          </div>

          {fullAddress && (
            <div className={styles.section}>
              <h3>Localização</h3>
              <p className={styles.addressText}>{fullAddress}</p>
            </div>
          )}

          {property.description && (
            <div className={styles.section}>
              <h3>Descrição</h3>
              <p className={styles.descriptionText}>{property.description}</p>
            </div>
          )}

          <div className={styles.contactSection}>
            <h3>Entre em contato</h3>
            <ContactForm propertyId={property.id} slug={slug} />
          </div>
        </div>
      </div>
    </ShowcaseLayout>
  );
}
