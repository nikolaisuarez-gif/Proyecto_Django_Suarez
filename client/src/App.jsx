import { Link, NavLink, Route, Routes } from 'react-router-dom'
import CatalogPage from './pages/CatalogPage.jsx'
import ProductFormPage from './pages/ProductFormPage.jsx'

export default function App() {
  return <div className="app-shell">
    <header className="site-header">
      <Link className="brand" to="/" aria-label="Suarez, inicio"><span className="brand-mark">S</span><span>suarez<span className="brand-dot">.</span><small>OBJETOS PARA CADA DÍA</small></span></Link>
      <nav><NavLink to="/" end>Catálogo</NavLink><NavLink className="nav-add" to="/productos/nuevo">Añadir producto <span>+</span></NavLink></nav>
    </header>
    <main><Routes><Route path="/" element={<CatalogPage />} /><Route path="/productos/nuevo" element={<ProductFormPage />} /><Route path="/productos/:id/editar" element={<ProductFormPage />} /></Routes></main>
    <footer><span>SUAREZ · CATÁLOGO 2026</span><span>Diseñado para elegir mejor.</span></footer>
  </div>
}
