import axios from 'axios'
const baseURL =
  window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "/api/";
const apiClient = axios.create({
  baseURL: baseURL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
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
  getEvents(projectId = null) {
    const params = projectId ? { project_id: projectId } : {}
    return apiClient.get('/events/', { params })
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
  baseURL() {
    return baseURL
  }
}
