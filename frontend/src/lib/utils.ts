// // """Utility functions for the frontend."""

// import { type ClassValue, clsx } from 'clsx'
// import { twMerge } from 'tailwind-merge'


// /**
//  * Merge Tailwind CSS classes with proper precedence
//  */
// export function cn(...inputs: ClassValue[]) {
//   return twMerge(clsx(inputs))
// }

// /**
//  * Format date to readable string
//  */
// export function formatDate(date: string | Date): string {
//   const d = typeof date === 'string' ? new Date(date) : date
//   return d.toLocaleDateString('en-US', {
//     year: 'numeric',
//     month: 'short',
//     day: 'numeric',
//   })
// }

// /**
//  * Format date to relative time (e.g., "2 hours ago")
//  */
// export function formatRelativeTime(date: string | Date): string {
//   const d = typeof date === 'string' ? new Date(date) : date
//   const now = new Date()
//   const diffMs = now.getTime() - d.getTime()
//   const diffSecs = Math.floor(diffMs / 1000)
//   const diffMins = Math.floor(diffSecs / 60)
//   const diffHours = Math.floor(diffMins / 60)
//   const diffDays = Math.floor(diffHours / 24)

//   if (diffSecs < 60) return 'just now'
//   if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`
//   if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`
//   if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`
//   return formatDate(d)
// }

// /**
//  * Truncate text to specified length
//  */
// export function truncate(text: string, length: number): string {
//   if (text.length <= length) return text
//   return text.slice(0, length) + '...'
// }

// /**
//  * Validate email format
//  */
// export function isValidEmail(email: string): boolean {
//   const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
//   return emailRegex.test(email)
// }

// /**
//  * Validate password strength
//  */
// export function isValidPassword(password: string): boolean {
//   // Minimum 8 characters, at least one letter and one number
//   return password.length >= 8 && /[a-zA-Z]/.test(password) && /[0-9]/.test(password)
// }










// """Utility functions for the frontend."""

import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

/**
 * Merge Tailwind CSS classes with proper precedence
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Format date to readable string
 */
export function formatDate(date: string | Date): string {
  const d = typeof date === 'string' ? new Date(date) : date
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

/**
 * Format date to relative time (e.g., "2 hours ago")
 */
export function formatRelativeTime(date?: string | Date): string {
  if (!date) return 'Unknown time' // missing date fallback

  const d = typeof date === 'string' ? new Date(date) : date
  const now = new Date()

  if (isNaN(d.getTime())) return 'Invalid date' // invalid string fallback

  const diffMs = now.getTime() - d.getTime()
  const diffSecs = Math.floor(diffMs / 1000)
  const diffMins = Math.floor(diffSecs / 60)
  const diffHours = Math.floor(diffMins / 60)
  const diffDays = Math.floor(diffHours / 24)

  if (diffSecs < 60) return 'just now'
  if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`
  if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`
  if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`

  return formatDate(d)
}

/**
 * Truncate text to specified length
 */
export function truncate(text: string, length: number): string {
  if (text.length <= length) return text
  return text.slice(0, length) + '...'
}

/**
 * Validate email format
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * Validate password strength
 */
export function isValidPassword(password: string): boolean {
  // Minimum 8 characters, at least one letter and one number
  return password.length >= 8 && /[a-zA-Z]/.test(password) && /[0-9]/.test(password)
}
