'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import apiClient, { setAuthToken } from '@/lib/api'
import type { SignUpRequest, AuthResponse } from '@/types/user'

interface SignUpFormProps {
  onSuccess?: () => void
}

export default function SignUpForm({ onSuccess }: SignUpFormProps) {
  const router = useRouter()
  const [error, setError] = useState<string>('')
  const [isLoading, setIsLoading] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignUpRequest>()

  const onSubmit = async (data: SignUpRequest) => {
    setIsLoading(true)
    setError('')

    try {
      const response = await apiClient.post<AuthResponse>('/api/auth/signup', data)
      const { token, user } = response.data

      // Store token
      setAuthToken(token)

      // Call success callback if provided
      if (onSuccess) {
        onSuccess()
      } else {
        // Redirect to tasks page
        router.push('/tasks')
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to create account'
      setError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
          Email
        </label>
        <input
          id="email"
          type="email"
          {...register('email', {
            required: 'Email is required',
            pattern: {
              value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
              message: 'Invalid email format',
            },
          })}
          className="input-field"
          placeholder="you@example.com"
        />
        {errors.email && (
          <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
          Password
        </label>
        <input
          id="password"
          type="password"
          {...register('password', {
            required: 'Password is required',
            minLength: {
              value: 8,
              message: 'Password must be at least 8 characters',
            },
            validate: {
              hasLetter: (value) =>
                /[a-zA-Z]/.test(value) || 'Password must contain at least one letter',
              hasNumber: (value) =>
                /[0-9]/.test(value) || 'Password must contain at least one number',
            },
          })}
          className="input-field"
          placeholder="••••••••"
        />
        {errors.password && (
          <p className="text-red-500 text-sm mt-1">{errors.password.message}</p>
        )}
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <button
        type="submit"
        disabled={isLoading}
        className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading ? 'Creating account...' : 'Sign Up'}
      </button>
    </form>
  )
}
