// 'use client'

// import { useState } from 'react'
// import apiClient from '@/lib/api'
// import { formatRelativeTime } from '@/lib/utils'
// import type { Task, UpdateTaskRequest } from '@/types/task'

// interface TaskItemProps {
//   task: Task
//   userId: string
//   onTaskUpdated: (task: Task) => void
//   onTaskDeleted: (taskId: number) => void
// }

// export default function TaskItem({ task, userId, onTaskUpdated, onTaskDeleted }: TaskItemProps) {
//   const [isEditing, setIsEditing] = useState(false)
//   const [editTitle, setEditTitle] = useState(task.title)
//   const [editDescription, setEditDescription] = useState(task.description || '')
//   const [isLoading, setIsLoading] = useState(false)
//   const [error, setError] = useState<string>('')

//   const handleToggleComplete = async () => {
//     setIsLoading(true)
//     setError('')

//     try {
//       const response = await apiClient.patch<Task>(
//         `/api/users/${userId}/tasks/${task.id}/complete`
//       )
//       onTaskUpdated(response.data)
//     } catch (err: any) {
//       setError('Failed to update task')
//     } finally {
//       setIsLoading(false)
//     }
//   }

//   const handleUpdate = async () => {
//     if (!editTitle.trim()) {
//       setError('Title cannot be empty')
//       return
//     }

//     setIsLoading(true)
//     setError('')

//     try {
//       const updateData: UpdateTaskRequest = {
//         title: editTitle.trim(),
//         description: editDescription.trim() || undefined,
//       }

//       const response = await apiClient.put<Task>(
//         `/api/users/${userId}/tasks/${task.id}`,
//         updateData
//       )
//       onTaskUpdated(response.data)
//       setIsEditing(false)
//     } catch (err: any) {
//       setError(err.response?.data?.detail || 'Failed to update task')
//     } finally {
//       setIsLoading(false)
//     }
//   }

//   const handleDelete = async () => {
//     if (!confirm('Are you sure you want to delete this task?')) {
//       return
//     }

//     setIsLoading(true)
//     setError('')

//     try {
//       await apiClient.delete(`/api/users/${userId}/tasks/${task.id}`)
//       onTaskDeleted(task.id)
//     } catch (err: any) {
//       setError('Failed to delete task')
//     } finally {
//       setIsLoading(false)
//     }
//   }

//   const handleCancel = () => {
//     setEditTitle(task.title)
//     setEditDescription(task.description || '')
//     setIsEditing(false)
//     setError('')
//   }

//   if (isEditing) {
//     return (
//       <div className="card">
//         <div className="space-y-3">
//           <div>
//             <input
//               type="text"
//               value={editTitle}
//               onChange={(e) => setEditTitle(e.target.value)}
//               className="input-field"
//               placeholder="Task title"
//               maxLength={200}
//             />
//           </div>
//           <div>
//             <textarea
//               value={editDescription}
//               onChange={(e) => setEditDescription(e.target.value)}
//               className="input-field"
//               placeholder="Task description (optional)"
//               rows={3}
//               maxLength={1000}
//             />
//           </div>

//           {error && (
//             <div className="text-red-500 text-sm">{error}</div>
//           )}

//           <div className="flex space-x-2">
//             <button
//               onClick={handleUpdate}
//               disabled={isLoading}
//               className="btn-primary disabled:opacity-50"
//             >
//               {isLoading ? 'Saving...' : 'Save'}
//             </button>
//             <button
//               onClick={handleCancel}
//               disabled={isLoading}
//               className="btn-secondary"
//             >
//               Cancel
//             </button>
//           </div>
//         </div>
//       </div>
//     )
//   }

//   return (
//     <div className={`card ${task.completed ? 'bg-gray-50' : ''}`}>
//       <div className="flex items-start space-x-3">
//         {/* Checkbox */}
//         <input
//           type="checkbox"
//           checked={task.completed}
//           onChange={handleToggleComplete}
//           disabled={isLoading}
//           className="mt-1 h-5 w-5 text-primary-600 rounded focus:ring-primary-500 cursor-pointer"
//         />

//         {/* Task Content */}
//         <div className="flex-1 min-w-0">
//           <h3
//             className={`text-lg font-medium ${
//               task.completed ? 'line-through text-gray-500' : 'text-gray-900'
//             }`}
//           >
//             {task.title}
//           </h3>
//           {task.description && (
//             <p className={`mt-1 text-sm ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
//               {task.description}
//             </p>
//           )}
//           <p className="mt-2 text-xs text-gray-400">
//             Created {formatRelativeTime(task.createdAt)}
//           </p>
//         </div>

//         {/* Actions */}
//         <div className="flex space-x-2">
//           <button
//             onClick={() => setIsEditing(true)}
//             disabled={isLoading}
//             className="text-primary-600 hover:text-primary-700 text-sm font-medium"
//           >
//             Edit
//           </button>
//           <button
//             onClick={handleDelete}
//             disabled={isLoading}
//             className="text-red-600 hover:text-red-700 text-sm font-medium"
//           >
//             Delete
//           </button>
//         </div>
//       </div>

//       {error && (
//         <div className="mt-2 text-red-500 text-sm">{error}</div>
//       )}
//     </div>
//   )
// }













'use client'

import { useState } from 'react'
import apiClient from '@/lib/api'
import { formatRelativeTime } from '@/lib/utils'
import type { Task, UpdateTaskRequest } from '@/types/task'

interface TaskItemProps {
  task: Task
  userId: string
  onTaskUpdated: (task: Task) => void
  onTaskDeleted: (taskId: number) => void
}

export default function TaskItem({ task, userId, onTaskUpdated, onTaskDeleted }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [editTitle, setEditTitle] = useState(task.title)
  const [editDescription, setEditDescription] = useState(task.description || '')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string>('')

  const handleToggleComplete = async () => {
    setIsLoading(true)
    setError('')
    try {
      const response = await apiClient.patch<Task>(`/api/users/${userId}/tasks/${task.id}/complete`)
      onTaskUpdated(response.data)
    } catch {
      setError('Failed to update task')
    } finally {
      setIsLoading(false)
    }
  }

  const handleUpdate = async () => {
    if (!editTitle.trim()) {
      setError('Title cannot be empty')
      return
    }

    setIsLoading(true)
    setError('')
    try {
      const updateData: UpdateTaskRequest = {
        title: editTitle.trim(),
        description: editDescription.trim() || undefined,
      }
      const response = await apiClient.put<Task>(`/api/users/${userId}/tasks/${task.id}`, updateData)
      onTaskUpdated(response.data)
      setIsEditing(false)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update task')
    } finally {
      setIsLoading(false)
    }
  }

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) return
    setIsLoading(true)
    setError('')
    try {
      await apiClient.delete(`/api/users/${userId}/tasks/${task.id}`)
      onTaskDeleted(task.id)
    } catch {
      setError('Failed to delete task')
    } finally {
      setIsLoading(false)
    }
  }

  const handleCancel = () => {
    setEditTitle(task.title)
    setEditDescription(task.description || '')
    setIsEditing(false)
    setError('')
  }

  if (isEditing) {
    return (
      <div className="card">
        <div className="space-y-3">
          <input
            type="text"
            value={editTitle}
            onChange={e => setEditTitle(e.target.value)}
            className="input-field"
            placeholder="Task title"
            maxLength={200}
          />
          <textarea
            value={editDescription}
            onChange={e => setEditDescription(e.target.value)}
            className="input-field"
            placeholder="Task description (optional)"
            rows={3}
            maxLength={1000}
          />
          {error && <div className="text-red-500 text-sm">{error}</div>}
          <div className="flex space-x-2">
            <button onClick={handleUpdate} disabled={isLoading} className="btn-primary disabled:opacity-50">
              {isLoading ? 'Saving...' : 'Save'}
            </button>
            <button onClick={handleCancel} disabled={isLoading} className="btn-secondary">Cancel</button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={`card ${task.completed ? 'bg-gray-50' : ''}`}>
      <div className="flex items-start space-x-3">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={handleToggleComplete}
          disabled={isLoading}
          className="mt-1 h-5 w-5 text-primary-600 rounded focus:ring-primary-500 cursor-pointer"
        />
        <div className="flex-1 min-w-0">
          <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`mt-1 text-sm ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
              {task.description}
            </p>
          )}
          <p className="mt-2 text-xs text-gray-400">
            Created {formatRelativeTime(task.createdAt)}
          </p>
        </div>
        <div className="flex space-x-2">
          <button onClick={() => setIsEditing(true)} disabled={isLoading} className="text-primary-600 hover:text-primary-700 text-sm font-medium">
            Edit
          </button>
          <button onClick={handleDelete} disabled={isLoading} className="text-red-600 hover:text-red-700 text-sm font-medium">
            Delete
          </button>
        </div>
      </div>
      {error && <div className="mt-2 text-red-500 text-sm">{error}</div>}
    </div>
  )
}
