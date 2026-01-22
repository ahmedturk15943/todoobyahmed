import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100">
      <div className="text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Welcome to Todo App
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Manage your tasks efficiently with our modern todo application
        </p>
        <div className="space-x-4">
          <Link
            href="/signin"
            className="inline-block bg-primary-600 text-white px-6 py-3 rounded-md hover:bg-primary-700 transition-colors"
          >
            Sign In
          </Link>
          <Link
            href="/signup"
            className="inline-block bg-white text-primary-600 px-6 py-3 rounded-md border-2 border-primary-600 hover:bg-primary-50 transition-colors"
          >
            Sign Up
          </Link>
        </div>
      </div>
    </div>
  )
}
