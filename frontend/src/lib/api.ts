/**
 * API client for communicating with the backend.
 */

import axios, { AxiosInstance, AxiosError } from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Create axios instance with default config
const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
})

// Request interceptor to add JWT token
apiClient.interceptors.request.use(
  config => {
    // Get token from localStorage or cookie
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
  response => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to signin
      localStorage.removeItem('auth_token')
      if (typeof window !== 'undefined') {
        window.location.href = '/signin'
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient

// Helper function to set auth token
export const setAuthToken = (token: string) => {
  localStorage.setItem('auth_token', token)
}

// Helper function to clear auth token
export const clearAuthToken = () => {
  localStorage.removeItem('auth_token')
}

// Helper function to get auth token
export const getAuthToken = (): string | null => {
  return localStorage.getItem('auth_token')
}
