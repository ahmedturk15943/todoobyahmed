'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import apiClient from '@/lib/api'
import type { Task, CreateTaskRequest } from '@/types/task'

interface TaskFormProps {
  userId: string
  onSuccess: (task: Task) => void
  onCancel?: () => void
}

export default function TaskForm({ userId, onSuccess, onCancel }: TaskFormProps) {
  const [error, setError] = useState<string>('')
  const [isLoading, setIsLoading] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<CreateTaskRequest>()

  const onSubmit = async (data: CreateTaskRequest) => {
    setIsLoading(true)
    setError('')

    try {
      const response = await apiClient.post<Task>(`/api/users/${userId}/tasks`, {
        title: data.title.trim(),
        description: data.description?.trim() || undefined,
      })

      reset()
      onSuccess(response.data)
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to create task'
      setError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="card">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            id="title"
            type="text"
            {...register('title', {
              required: 'Title is required',
              minLength: {
                value: 1,
                message: 'Title must be at least 1 character',
              },
              maxLength: {
                value: 200,
                message: 'Title must be at most 200 characters',
              },
            })}
            className="input-field"
            placeholder="What needs to be done?"
            maxLength={200}
          />
          {errors.title && (
            <p className="text-red-500 text-sm mt-1">{errors.title.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description (optional)
          </label>
          <textarea
            id="description"
            {...register('description', {
              maxLength: {
                value: 1000,
                message: 'Description must be at most 1000 characters',
              },
            })}
            className="input-field"
            placeholder="Add more details..."
            rows={3}
            maxLength={1000}
          />
          {errors.description && (
            <p className="text-red-500 text-sm mt-1">{errors.description.message}</p>
          )}
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        <div className="flex space-x-2">
          <button
            type="submit"
            disabled={isLoading}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Creating...' : 'Create Task'}
          </button>
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              disabled={isLoading}
              className="btn-secondary"
            >
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  )
}
