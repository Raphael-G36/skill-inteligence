'use client'

import { useState, FormEvent } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import InfoTooltip from '@/components/InfoTooltip'
import InfoBox from '@/components/InfoBox'

export default function AnalyzePage() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    role: '',
    industry: '',
    region: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsSubmitting(true)
    setError(null)

    try {
      // Navigate to results page with query parameters
      // Note: Data is passed via URL params only - no local storage to maintain privacy
      const params = new URLSearchParams({
        role: formData.role.trim(),
        industry: formData.industry.trim(),
        region: formData.region.trim()
      })
      
      router.push(`/results?${params.toString()}`)
    } catch (err) {
      setError('Failed to submit form. Please try again.')
      setIsSubmitting(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      {/* Navigation */}
      <nav className="border-b border-gray-200 dark:border-gray-700 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="flex items-center">
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Skill Intelligence
              </h1>
            </Link>
            <div className="flex items-center space-x-4">
              <Link
                href="/"
                className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
              >
                Home
              </Link>
              <Link
                href="/analyze"
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors"
              >
                Analyze
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="flex flex-col items-center justify-center px-4 py-12 min-h-[calc(100vh-4rem)]">
        <div className="w-full max-w-2xl">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
              Analyze Your Skills
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-300">
              Enter your role, industry, and region to discover the most in-demand skills
            </p>
          </div>

          {/* Guidance Info Box */}
          <div className="mb-6">
            <InfoBox
              message="Enter your role and industry. Some niche roles may not return results. Results are based on limited sample data and should be used as a reference only."
              type="warning"
              dismissible={true}
            />
          </div>

          {/* Form Card */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 md:p-10 border border-gray-200 dark:border-gray-700">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Role Input */}
              <div>
                <label 
                  htmlFor="role" 
                  className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2"
                >
                  <span className="flex items-center gap-2">
                    Role *
                    <InfoTooltip 
                      message="Enter your job role (e.g., Backend Engineer, Data Scientist). Some niche or very new roles may have limited data available."
                      position="top"
                    />
                  </span>
                </label>
                <input
                  type="text"
                  id="role"
                  name="role"
                  value={formData.role}
                  onChange={handleChange}
                  required
                  placeholder="e.g., Backend Engineer, Frontend Developer, Data Scientist"
                  className="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-xl 
                           focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                           bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                           placeholder-gray-400 dark:placeholder-gray-500
                           transition-all duration-200"
                />
              </div>

              {/* Industry Input */}
              <div>
                <label 
                  htmlFor="industry" 
                  className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2"
                >
                  <span className="flex items-center gap-2">
                    Industry *
                    <InfoTooltip 
                      message="Enter the industry sector you work in (e.g., FinTech, Healthcare, E-commerce). Results may vary based on industry-specific data availability."
                      position="top"
                    />
                  </span>
                </label>
                <input
                  type="text"
                  id="industry"
                  name="industry"
                  value={formData.industry}
                  onChange={handleChange}
                  required
                  placeholder="e.g., FinTech, E-commerce, Healthcare, SaaS"
                  className="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-xl 
                           focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                           bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                           placeholder-gray-400 dark:placeholder-gray-500
                           transition-all duration-200"
                />
              </div>

              {/* Region Input */}
              <div>
                <label 
                  htmlFor="region" 
                  className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2"
                >
                  <span className="flex items-center gap-2">
                    Region *
                    <InfoTooltip 
                      message="Select the geographic region. Global data provides broader insights, while regional data focuses on specific markets."
                      position="top"
                    />
                  </span>
                </label>
                <select
                  id="region"
                  name="region"
                  value={formData.region}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-xl 
                           focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                           bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                           transition-all duration-200"
                >
                  <option value="">Select a region</option>
                  <option value="Global">Global</option>
                  <option value="North America">North America</option>
                  <option value="Europe">Europe</option>
                  <option value="Asia Pacific">Asia Pacific</option>
                  <option value="Latin America">Latin America</option>
                  <option value="Middle East & Africa">Middle East & Africa</option>
                </select>
              </div>

              {/* Error Message */}
              {error && (
                <div className="p-4 bg-red-50 dark:bg-red-900/20 border-2 border-red-200 dark:border-red-800 rounded-xl">
                  <p className="text-sm text-red-600 dark:text-red-400 font-medium">{error}</p>
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 
                         disabled:from-gray-400 disabled:to-gray-500
                         text-white font-semibold py-4 px-6 rounded-xl 
                         transition-all duration-200 transform hover:scale-[1.02] disabled:scale-100
                         focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
                         dark:focus:ring-offset-gray-800 shadow-lg hover:shadow-xl disabled:shadow-none"
              >
                {isSubmitting ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Analyzing...
                  </span>
                ) : (
                  'Analyze Skills →'
                )}
              </button>
            </form>
          </div>

          {/* Info Section */}
          <div className="mt-8 text-center">
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">
              Get insights into top skills, trending technologies, and personalized recommendations
            </p>
            <Link href="/" className="text-sm text-blue-600 dark:text-blue-400 hover:underline">
              ← Back to Home
            </Link>
          </div>
        </div>
      </div>
    </main>
  )
}

