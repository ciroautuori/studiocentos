import axios from 'axios'
const baseURL =
  window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "/api/";
const apiClient = axios.create({
  baseURL: baseURL,
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
})

export default {
  async login(username, password) {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)

    try {
      const response = await apiClient.post('/token', formData)
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token)
        return response.data
      }
    } catch (error) {
      throw error
    }
  },

  logout() {
    localStorage.removeItem('token')
  },

  getToken() {
    return localStorage.getItem('token')
  },

  isAuthenticated() {
    return !!this.getToken()
  }
}
