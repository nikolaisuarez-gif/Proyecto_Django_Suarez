import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import categoryService from '../services/categoryService.js'
import productService from '../services/productService.js'

const initialForm = { name: '', description: '', price: '', stock: '', category_id: '', image: null }

export default function ProductFormPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [form, setForm] = useState(initialForm)
  const [categories, setCategories] = useState([])
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    async function loadForm() {
      try {
        const categoryData = await categoryService.list()
        setCategories(categoryData.results ?? categoryData)
        if (id) {
          const product = await productService.get(id)
          setForm({ name: product.name, description: product.description, price: product.price, stock: product.stock, category_id: product.category.id, image: null })
        }
      } catch { setError('No se pudieron cargar los datos del formulario.') }
    }
    loadForm()
  }, [id])

  function updateField(event) {
    const { name, value, files } = event.target
    setForm(current => ({ ...current, [name]: files ? files[0] : value }))
  }

  async function submit(event) {
    event.preventDefault(); setSaving(true); setError('')
    const payload = new FormData()
    Object.entries(form).forEach(([key, value]) => { if (value !== null && value !== '') payload.append(key, value) })
    try {
      if (id) await productService.update(id, payload)
      else await productService.create(payload)
      navigate('/')
    } catch (requestError) {
      const detail = requestError.response?.data
      setError(detail ? Object.values(detail).flat().join(' ') : 'No se pudo guardar el producto. Verifica los datos y vuelve a intentar.')
    } finally { setSaving(false) }
  }

  return <section className="form-page"><Link className="back-link" to="/">← Volver al catálogo</Link><span className="eyebrow">GESTIÓN DE PRODUCTOS</span><h1>{id ? 'Editar producto' : 'Nuevo producto'}</h1><p className="form-intro">Completa los detalles para que aparezca en el catálogo.</p>
    {error && <p className="inline-error" role="alert">{error}</p>}
    <form className="product-form" onSubmit={submit}>
      <label>Nombre del producto<input required name="name" value={form.name} onChange={updateField} maxLength="140" /></label>
      <label>Categoría<select required name="category_id" value={form.category_id} onChange={updateField}><option value="">Selecciona una categoría</option>{categories.map(item => <option key={item.id} value={item.id}>{item.name}</option>)}</select></label>
      <label className="wide-field">Descripción<textarea required name="description" value={form.description} onChange={updateField} rows="4" /></label>
      <label>Precio (S/)<input required type="number" name="price" min="0" step="0.01" value={form.price} onChange={updateField} /></label>
      <label>Existencias<input required type="number" name="stock" min="0" step="1" value={form.stock} onChange={updateField} /></label>
      <label className="wide-field">Imagen del producto<input type="file" name="image" accept="image/*" onChange={updateField} /><small>Opcional. Si no eliges otra, conservaremos la imagen actual.</small></label>
      <div className="form-actions"><Link to="/">Cancelar</Link><button className="button-primary" disabled={saving || categories.length === 0}>{saving ? 'Guardando...' : 'Guardar producto'}</button></div>
    </form>
  </section>
}
