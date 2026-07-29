import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import publicApi from '../services/publicApi';
import ShowcaseLayout from '../components/showcaseLayout/showcaseLayout';
import PropertyCard from '../components/propertyCard/propertyCard';
import styles from './ShowcaseList.module.css';

export default function ShowcaseList() {
  const { slug } = useParams();
  const [info, setInfo] = useState(null);
  const [properties, setProperties] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    publicApi.get(`/${slug}/info`)
      .then(res => setInfo(res.data))
      .catch(() => setError('Corretora não encontrada'));
  }, [slug]);

  useEffect(() => {
    if (!info) return;
    setLoading(true);
    publicApi.get(`/${slug}/properties`, { params: { page, page_size: 12 } })
      .then(res => {
        setProperties(res.data.data);
        setTotalPages(res.data.pagination.total_pages);
      })
      .catch(() => setError('Erro ao carregar imóveis'))
      .finally(() => setLoading(false));
  }, [slug, page, info]);

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  if (!info) {
    return <div className={styles.loading}>Carregando...</div>;
  }

  return (
    <ShowcaseLayout info={info}>
      {loading ? (
        <div className={styles.loading}>Carregando imóveis...</div>
      ) : properties.length === 0 ? (
        <div className={styles.empty}>Nenhum imóvel encontrado</div>
      ) : (
        <>
          <div className={styles.grid}>
            {properties.map(property => (
              <PropertyCard key={property.id} property={property} slug={slug} />
            ))}
          </div>
          <div className={styles.pagination}>
            <button
              onClick={() => setPage(p => p - 1)}
              disabled={page === 1}
            >
              Anterior
            </button>
            <span>Página {page} de {totalPages}</span>
            <button
              onClick={() => setPage(p => p + 1)}
              disabled={page === totalPages}
            >
              Próxima
            </button>
          </div>
        </>
      )}
    </ShowcaseLayout>
  );
}
