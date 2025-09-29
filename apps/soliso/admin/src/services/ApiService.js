import axios from 'axios'
import AuthService from './AuthService'
const baseURL =
  window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "/api/";
const apiClient = axios.create({
  baseURL: baseURL,
  headers: {
    // Lascia che axios imposti Content-Type dinamicamente (es. multipart/form-data se usi FormData)
  },
})

// Interceptor per aggiungere il token di autenticazione
apiClient.interceptors.request.use(
  (config) => {
    const token = AuthService.getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor per gestire gli errori di autenticazione
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      AuthService.logout()
      window.location.href = '/login'
    }
    console.error('API call error:', error.response || error.message)
    return Promise.reject(error)
  },
)

export default {
  // --- Projects API ---
  getProjects() {
    return apiClient.get('/projects/')
  },
  getProject(id) {
    return apiClient.get(`/projects/${id}`)
  },
  createProject(projectData) {
    const isFormData = projectData instanceof FormData
    return apiClient.post('/projects/', projectData, {
      headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : {},
    })
  },
  updateProject(id, projectData) {
    const isFormData = projectData instanceof FormData
    return apiClient.put(`/projects/${id}`, projectData, {
      headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : {},
    })
  },
  deleteProject(id) {
    return apiClient.delete(`/projects/${id}`)
  },

  // --- Events API ---
  getEvents() {
    return apiClient.get('/events/')
  },
  getEvent(id) {
    return apiClient.get(`/events/${id}`)
  },
  createEvent(eventData) {
    const isFormData = eventData instanceof FormData
    return apiClient.post('/events/', eventData, {
      headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : {},
    })
  },
  updateEvent(id, eventData) {
    const isFormData = eventData instanceof FormData
    return apiClient.put(`/events/${id}`, eventData, {
      headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : {},
    })
  },
  deleteEvent(id) {
    return apiClient.delete(`/events/${id}`)
  },
}
