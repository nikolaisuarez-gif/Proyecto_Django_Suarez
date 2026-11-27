import apiClient from './apiClient.js'

const categoryService = {
  async list() {
    const data = (await apiClient.get('/categories/')).data
    return data.results ?? data
  },
  async get(id) { return (await apiClient.get(`/categories/${id}/`)).data },
  async create(data) { return (await apiClient.post('/categories/', data)).data },
  async update(id, data) { return (await apiClient.patch(`/categories/${id}/`, data)).data },
  async remove(id) { return apiClient.delete(`/categories/${id}/`) },
}

export default categoryService
