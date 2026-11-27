import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import categoryService from '../services/categoryService.js'
import productService from '../services/productService.js'
import ProductCard from '../components/ProductCard.jsx'

export default function CatalogPage() {
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [category, setCategory] = useState('')
  const [status, setStatus] = useState('loading')
  const [error, setError] = useState('')

  const loadCatalog = useCallback(async () => {
    setStatus('loading'); setError('')
    try {
      const [productData, categoryData] = await Promise.all([
        productService.list(category ? { category } : {}), categoryService.list(),
      ])
      setProducts(productData.results ?? productData)
      setCategories(categoryData.results ?? categoryData)
      setStatus('success')
    } catch {
      setError('No pudimos conectar con el catálogo. Revisa que el servidor Django esté activo.')
      setStatus('error')
    }
  }, [category])

  useEffect(() => { loadCatalog() }, [loadCatalog])

  async function deleteProduct(product) {
    if (!window.confirm(`¿Eliminar ${product.name}?`)) return
    try { await productService.remove(product.id); await loadCatalog() }
    catch { setError('No se pudo eliminar el producto. Inténtalo otra vez.') }
  }

  return <>
    <section className="hero"><div className="hero-copy"><span className="eyebrow"><i /> COLECCIÓN 2026</span><h1>Lo cotidiano,<br /><em>mejor elegido.</em></h1><p>Una selección de objetos útiles, bien pensados y listos para acompañarte.</p><a className="text-link" href="#catalogo">Explorar catálogo <span>↓</span></a></div><div className="hero-art" aria-label="Composición gráfica de objetos cotidianos"><div className="art-orbit orbit-one"/><div className="art-orbit orbit-two"/><div className="art-block block-blue"/><div className="art-block block-orange"/><div className="art-circle"><span>S</span></div><span className="art-caption">OBJETOS<br />CON INTENCIÓN</span><span className="art-number">01 — 08</span></div></section>
    <section id="catalogo" className="catalog-section"><div className="section-heading"><div><span className="eyebrow">SELECCIÓN DE TEMPORADA</span><h2>El catálogo <span>({products.length})</span></h2></div><label className="filter-label">Filtrar por categoría <select value={category} onChange={event => setCategory(event.target.value)}><option value="">Todas las categorías</option>{categories.map(item => <option key={item.id} value={item.id}>{item.name}</option>)}</select></label></div>
      {status === 'loading' && <div className="notice">Cargando productos...</div>}
      {status === 'error' && <div className="notice notice-error" role="alert">{error}<button onClick={loadCatalog}>Volver a intentar</button></div>}
      {status === 'success' && products.length === 0 && <div className="notice">Aún no hay productos en esta categoría. <Link to="/productos/nuevo">Añade el primero.</Link></div>}
      {status === 'success' && products.length > 0 && <div className="product-grid">{products.map(product => <ProductCard key={product.id} product={product} onDelete={deleteProduct} />)}</div>}
    </section>
    {error && status === 'success' && <p className="inline-error" role="alert">{error}</p>}
  </>
}
