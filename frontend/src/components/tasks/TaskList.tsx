// 'use client'

// import { useState } from 'react'
// import TaskItem from './TaskItem'
// import type { Task } from '@/types/task'

// interface TaskListProps {
//   tasks: Task[]
//   userId: string
//   onTaskUpdated: (task: Task) => void
//   onTaskDeleted: (taskId: number) => void
// }

// export default function TaskList({ tasks, userId, onTaskUpdated, onTaskDeleted }: TaskListProps) {
//   const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all')

//   const filteredTasks = tasks.filter(task => {
//     if (filter === 'active') return !task.completed
//     if (filter === 'completed') return task.completed
//     return true
//   })

//   if (tasks.length === 0) {
//     return (
//       <div className="text-center py-12">
//         <svg
//           className="mx-auto h-12 w-12 text-gray-400"
//           fill="none"
//           viewBox="0 0 24 24"
//           stroke="currentColor"
//         >
//           <path
//             strokeLinecap="round"
//             strokeLinejoin="round"
//             strokeWidth={2}
//             d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
//           />
//         </svg>
//         <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
//         <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
//       </div>
//     )
//   }

//   return (
//     <div>
//       {/* Filter Tabs */}
//       <div className="mb-4 border-b border-gray-200">
//         <nav className="-mb-px flex space-x-8">
//           <button
//             onClick={() => setFilter('all')}
//             className={`${
//               filter === 'all'
//                 ? 'border-primary-500 text-primary-600'
//                 : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
//             } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
//           >
//             All ({tasks.length})
//           </button>
//           <button
//             onClick={() => setFilter('active')}
//             className={`${
//               filter === 'active'
//                 ? 'border-primary-500 text-primary-600'
//                 : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
//             } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
//           >
//             Active ({tasks.filter(t => !t.completed).length})
//           </button>
//           <button
//             onClick={() => setFilter('completed')}
//             className={`${
//               filter === 'completed'
//                 ? 'border-primary-500 text-primary-600'
//                 : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
//             } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
//           >
//             Completed ({tasks.filter(t => t.completed).length})
//           </button>
//         </nav>
//       </div>

//       {/* Task Items */}
//       <div className="space-y-3">
//         {filteredTasks.map(task => (
//           <TaskItem
//             key={task.id}
//             task={task}
//             userId={userId}
//             onTaskUpdated={onTaskUpdated}
//             onTaskDeleted={onTaskDeleted}
//           />
//         ))}
//       </div>

//       {filteredTasks.length === 0 && (
//         <div className="text-center py-8 text-gray-500">
//           No {filter} tasks
//         </div>
//       )}
//     </div>
//   )
// }











'use client'

import { useState, useMemo } from 'react'
import TaskItem from './TaskItem'
import type { Task } from '@/types/task'

interface TaskListProps {
  tasks: Task[]
  userId: string
  onTaskUpdated: (task: Task) => void
  onTaskDeleted: (taskId: number) => void
}

export default function TaskList({ tasks, userId, onTaskUpdated, onTaskDeleted }: TaskListProps) {
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all')

  // ✅ useMemo to avoid recalculating filtered tasks on every render
  const filteredTasks = useMemo(() => {
    return tasks.filter(task => {
      if (filter === 'active') return !task.completed
      if (filter === 'completed') return task.completed
      return true
    })
  }, [tasks, filter])

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
        </svg>
        <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
        <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
      </div>
    )
  }

  return (
    <div>
      {/* Filter Tabs */}
      <div className="mb-4 border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {['all', 'active', 'completed'].map(f => (
            <button
              key={f}
              onClick={() => setFilter(f as 'all' | 'active' | 'completed')}
              className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
                filter === f
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)} ({f === 'all' ? tasks.length : f === 'active' ? tasks.filter(t => !t.completed).length : tasks.filter(t => t.completed).length})
            </button>
          ))}
        </nav>
      </div>

      {/* Task Items */}
      <div className="space-y-3">
        {filteredTasks.map(task => (
          <TaskItem
            key={task.id}
            task={task}
            userId={userId}
            onTaskUpdated={onTaskUpdated}
            onTaskDeleted={onTaskDeleted}
          />
        ))}
      </div>

      {filteredTasks.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No {filter} tasks
        </div>
      )}
    </div>
  )
}
