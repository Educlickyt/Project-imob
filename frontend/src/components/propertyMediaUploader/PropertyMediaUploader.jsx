import { useState, useEffect } from 'react'
import api from '../../services/api'
import styles from './PropertyMediaUploader.module.css'

const PropertyMediaUploader = () => {
  const [properties, setProperties] = useState([])
  const [selectedPropertyId, setSelectedPropertyId] = useState('')
  const [medias, setMedias] = useState([])
  const [uploading, setUploading] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    api.get('/properties/')
      .then(res => {
        const list = Array.isArray(res.data) ? res.data : [res.data].filter(Boolean)
        setProperties(list)
        if (list.length === 1) setSelectedPropertyId(list[0].id)
      })
      .catch(() => setError('Erro ao carregar imóveis'))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    if (!selectedPropertyId) return
    api.get(`/properties/${selectedPropertyId}/media`)
      .then(res => setMedias(res.data))
      .catch(() => setError('Erro ao carregar mídias'))
  }, [selectedPropertyId])

  const handleFileChange = async (e) => {
    const file = e.target.files[0]
    if (!file || !selectedPropertyId) return

    setUploading(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('file', file)
      const res = await api.post(`/properties/${selectedPropertyId}/media`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setMedias(prev => [...prev, res.data])
    } catch (err) {
      setError('Erro ao fazer upload')
    } finally {
      setUploading(false)
      e.target.value = ''
    }
  }

  const handleDelete = async (mediaId) => {
    if (!selectedPropertyId) return
    try {
      await api.delete(`/properties/${selectedPropertyId}/media/${mediaId}`)
      setMedias(prev => prev.filter(m => m.id !== mediaId))
    } catch {
      setError('Erro ao excluir imagem')
    }
  }

  const handleSetCover = async (mediaId) => {
    if (!selectedPropertyId) return
    try {
      const res = await api.patch(`/properties/${selectedPropertyId}/media/${mediaId}/cover`)
      setMedias(prev => prev.map(m => ({
        ...m,
        is_cover: m.id === res.data.id,
      })))
    } catch {
      setError('Erro ao definir capa')
    }
  }

  if (loading) return <div className={styles.container}><p>Carregando...</p></div>

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Imagens dos Imóveis</h2>

      {error && <p className={styles.error}>{error}</p>}

      <div className={styles.selector}>
        <label>Imóvel:</label>
        <select
          value={selectedPropertyId}
          onChange={e => setSelectedPropertyId(e.target.value)}
        >
          <option value="">Selecione um imóvel</option>
          {properties.map(p => (
            <option key={p.id} value={p.id}>{p.title} ({p.slug})</option>
          ))}
        </select>
      </div>

      {selectedPropertyId && (
        <>
          <div className={styles.uploadArea}>
            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              disabled={uploading}
              id="file-input"
              className={styles.fileInput}
            />
            <label htmlFor="file-input" className={styles.fileLabel}>
              {uploading ? 'Enviando...' : 'Selecionar imagem'}
            </label>
          </div>

          <div className={styles.grid}>
            {medias.map(media => (
              <div key={media.id} className={styles.card}>
                <img
                  src={`http://localhost:8000/media/${media.id}`}
                  alt=""
                  className={styles.image}
                />
                <div className={styles.actions}>
                  {media.is_cover ? (
                    <span className={styles.coverBadge}>Capa</span>
                  ) : (
                    <button
                      className={styles.coverBtn}
                      onClick={() => handleSetCover(media.id)}
                    >
                      Definir como capa
                    </button>
                  )}
                  <button
                    className={styles.deleteBtn}
                    onClick={() => handleDelete(media.id)}
                  >
                    Excluir
                  </button>
                </div>
              </div>
            ))}
          </div>

          {medias.length === 0 && (
            <p className={styles.empty}>Nenhuma imagem cadastrada.</p>
          )}
        </>
      )}
    </div>
  )
}

export default PropertyMediaUploader
