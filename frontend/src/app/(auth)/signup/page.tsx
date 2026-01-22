import Link from 'next/link'
import SignUpForm from '@/components/auth/SignUpForm'

export default function SignUpPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100">
      <div className="card max-w-md w-full">
        <h1 className="text-3xl font-bold text-center mb-6">Create Account</h1>
        <SignUpForm />
        <p className="text-center text-gray-600 mt-6">
          Already have an account?{' '}
          <Link href="/signin" className="text-primary-600 hover:text-primary-700 font-medium">
            Sign In
          </Link>
        </p>
      </div>
    </div>
  )
}
