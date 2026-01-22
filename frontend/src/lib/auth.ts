// """Better Auth configuration for JWT authentication."""

// This file will be implemented when we add Better Auth integration
// For now, we'll use a simple JWT token approach

export const authConfig = {
  secret: process.env.BETTER_AUTH_SECRET || '',
  baseURL: process.env.BETTER_AUTH_URL || 'http://localhost:3000',
  expiryDays: 7,
}

// Helper to check if user is authenticated
export const isAuthenticated = (): boolean => {
  if (typeof window === 'undefined') return false
  const token = localStorage.getItem('auth_token')
  return !!token
}

// Helper to get current user from token (simplified)
export const getCurrentUser = (): { id: string; email: string } | null => {
  if (typeof window === 'undefined') return null
  const token = localStorage.getItem('auth_token')
  if (!token) return null

  try {
    // Decode JWT token (simplified - in production use a proper JWT library)
    const payload = JSON.parse(atob(token.split('.')[1]))
    return {
      id: payload.sub,
      email: payload.email,
    }
  } catch {
    return null
  }
}
