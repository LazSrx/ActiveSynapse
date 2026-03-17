import axios from 'axios'
import { useAuthStore } from '../stores/authStore'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        const refreshToken = useAuthStore.getState().refreshToken
        if (!refreshToken) {
          useAuthStore.getState().logout()
          return Promise.reject(error)
        }

        const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        })

        const { access_token, refresh_token } = response.data
        const user = useAuthStore.getState().user
        
        if (user) {
          useAuthStore.getState().setAuth(user, access_token, refresh_token)
        }

        originalRequest.headers.Authorization = `Bearer ${access_token}`
        return api(originalRequest)
      } catch (refreshError) {
        useAuthStore.getState().logout()
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default api

// Auth API
export const authApi = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  
  register: (data: { username: string; email: string; password: string }) =>
    api.post('/auth/register', data),
  
  refresh: (refreshToken: string) =>
    api.post('/auth/refresh', { refresh_token: refreshToken }),
  
  logout: () => api.post('/auth/logout'),
}

// User API
export const userApi = {
  getMe: () => api.get('/users/me'),
  updateMe: (data: any) => api.put('/users/me', data),
  getProfile: () => api.get('/users/me/profile'),
  updateProfile: (data: any) => api.put('/users/me/profile', data),
}

// Sport Records API
export const sportApi = {
  getRecords: (params?: any) => api.get('/sports/records', { params }),
  createRecord: (data: any) => api.post('/sports/records', data),
  updateRecord: (id: number, data: any) => api.put(`/sports/records/${id}`, data),
  deleteRecord: (id: number) => api.delete(`/sports/records/${id}`),
  getStatistics: (params?: any) => api.get('/sports/statistics', { params }),
  getWeeklySummary: () => api.get('/sports/weekly-summary'),
}

// Injury Records API
export const injuryApi = {
  getRecords: (params?: any) => api.get('/injuries/', { params }),
  createRecord: (data: any) => api.post('/injuries/', data),
  updateRecord: (id: number, data: any) => api.put(`/injuries/${id}`, data),
  deleteRecord: (id: number) => api.delete(`/injuries/${id}`),
  getSummary: () => api.get('/injuries/summary/statistics'),
}
