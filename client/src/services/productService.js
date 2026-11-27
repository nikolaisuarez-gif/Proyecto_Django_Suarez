import apiClient from './apiClient.js'

const productService = {
  async list(params = {}) { return (await apiClient.get('/products/', { params })).data },
  async get(id) { return (await apiClient.get(`/products/${id}/`)).data },
  async create(data) { return (await apiClient.post('/products/', data)).data },
  async update(id, data) { return (await apiClient.patch(`/products/${id}/`, data)).data },
  async remove(id) { return apiClient.delete(`/products/${id}/`) },
}

export default productService
