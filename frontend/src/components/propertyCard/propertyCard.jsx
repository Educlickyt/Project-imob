import { Link } from 'react-router-dom';
import styles from './propertyCard.module.css';

export default function PropertyCard({ property, slug }) {

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

  const transactionLabel = property.transaction_type === 'rent' ? '/mês' : '';

  return (
    <Link to={`/v/${slug}/${property.id}`} className={styles.card}>
      <div className={styles.imageContainer}>
        {property.medias && property.medias.length > 0 ? (
          <img
            src={`http://localhost:8000/media/${property.medias[0].id}`}
            alt={property.title}
            className={styles.image}
          />
        ) : (
          <div className={styles.noImage}>Sem imagem</div>
        )}
        {property.transaction_type && (
          <span className={styles.badge}>
            {property.transaction_type === 'sale' ? 'Venda' : 'Aluguel'}
          </span>
        )}
      </div>
      <div className={styles.info}>
        <h3 className={styles.title}>{property.title}</h3>
        <p className={styles.price}>{formattedPrice}{transactionLabel}</p>
        <div className={styles.details}>
          {property.bedrooms != null && <span>{property.bedrooms} quartos</span>}
          {property.garage_spots != null && <span>{property.garage_spots} vagas</span>}
          {property.area != null && <span>{property.area}m²</span>}
        </div>
        <p className={styles.address}>
          {[property.district, property.city].filter(Boolean).join(', ')}
        </p>
      </div>
    </Link>
  );
}
