import { Link } from 'react-router-dom'

export default function ProductCard({ product, onDelete }) {
  const imageUrl = product.image?.startsWith('http') ? product.image : `http://127.0.0.1:8000${product.image}`
  return <article className="product-card">
    <div className="product-image-wrap"><img src={imageUrl} alt={product.name} /><span className="image-index">{String(product.id).padStart(2, '0')}</span></div>
    <div className="product-meta"><span>{product.category?.name ?? 'Sin categoría'}</span><span>{product.stock > 0 ? 'Disponible' : 'Agotado'}</span></div>
    <h3>{product.name}</h3><p className="product-description">{product.description}</p>
    <div className="product-bottom"><strong>S/ {Number(product.price).toFixed(2)}</strong><div className="product-actions"><Link to={`/productos/${product.id}/editar`} aria-label={`Editar ${product.name}`}>Editar</Link><button type="button" onClick={() => onDelete(product)} aria-label={`Eliminar ${product.name}`}>Eliminar</button></div></div>
  </article>
}
