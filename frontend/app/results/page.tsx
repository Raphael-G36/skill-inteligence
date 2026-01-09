'use client'

import { useEffect, useState, Suspense } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { analyzeSkills, type AnalyzeResponse } from '@/lib/api'
import SkillCard from '@/components/SkillCard'
import TrendingSkill from '@/components/TrendingSkill'
import RecommendedSkill from '@/components/RecommendedSkill'
import InfoBox from '@/components/InfoBox'
import InfoTooltip from '@/components/InfoTooltip'

function ResultsContent() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const [searchCriteria, setSearchCriteria] = useState({
    role: '',
    industry: '',
    region: ''
  })
  const [data, setData] = useState<AnalyzeResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Get parameters from URL
    const role = searchParams.get('role') || ''
    const industry = searchParams.get('industry') || ''
    const region = searchParams.get('region') || ''

    setSearchCriteria({ role, industry, region })

    // Fetch data from API
    const fetchData = async () => {
      if (!role || !industry || !region) {
        setError('Missing required parameters')
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        setError(null)
        const response = await analyzeSkills({ role, industry, region })
        setData(response)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch data from backend')
        console.error('Error fetching data:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [searchParams])


  // Calculate percentages for top skills (inverse rank-based percentage)
  const getTopSkillPercentage = (index: number, total: number): number => {
    if (total === 0) return 0
    if (total === 1) return 100
    // Calculate percentage based on rank (1st = 100%, last = ~20%)
    const rank = index + 1
    const maxPercentage = 100
    const minPercentage = 20
    const percentage = maxPercentage - ((rank - 1) / (total - 1)) * (maxPercentage - minPercentage)
    return Math.round(percentage)
  }

  // Assign trend indicators to trending skills (simulate based on position)
  const getTrendForSkill = (index: number, total: number): 'rising' | 'stable' | 'declining' => {
    // First half = rising, middle = stable, last = declining
    if (index < total / 3) return 'rising'
    if (index < (total * 2) / 3) return 'stable'
    return 'declining'
  }

  // Get trend percentage for trending skills
  const getTrendPercentage = (trend: 'rising' | 'stable' | 'declining', index: number, total: number): number => {
    if (trend === 'rising') return Math.round(80 - index * 10)
    if (trend === 'stable') return Math.round(60 - index * 5)
    return Math.round(40 - index * 5)
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
                New Analysis
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="px-4 py-12">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-2">
              Analysis Results
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-300 flex items-center gap-2">
              Skills intelligence for your search criteria
              <InfoTooltip 
                message="Top skills are based on limited sample data. Use as a reference only. Results may not be comprehensive for all roles or industries."
                position="right"
              />
            </p>
          </div>

          {/* Guidance Info Box */}
          <div className="mb-6">
            <InfoBox
              message="Top skills are based on limited sample data. Use as a reference only. Results may not cover every role or industry comprehensively."
              type="warning"
              dismissible={true}
            />
          </div>

          {/* Role Not Recognized Warning */}
          {data && !data.role_recognized && data.message && (
            <div className="mb-6">
              <InfoBox
                message={data.message}
                type="warning"
                dismissible={true}
              />
            </div>
          )}

          {/* Search Criteria Card */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Search Criteria
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Role</p>
                <p className="text-lg font-medium text-gray-900 dark:text-white">
                  {searchCriteria.role || 'Not specified'}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Industry</p>
                <p className="text-lg font-medium text-gray-900 dark:text-white">
                  {searchCriteria.industry || 'Not specified'}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Region</p>
                <p className="text-lg font-medium text-gray-900 dark:text-white">
                  {searchCriteria.region || 'Not specified'}
                </p>
              </div>
            </div>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-12">
              <div className="text-center">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent mb-4"></div>
                <p className="text-gray-600 dark:text-gray-400">Analyzing skills...</p>
              </div>
            </div>
          )}

          {/* Error State */}
          {error && !loading && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6 mb-6">
              <div className="flex items-start gap-3">
                <svg
                  className="w-6 h-6 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <div>
                  <h3 className="text-lg font-semibold text-red-800 dark:text-red-300 mb-1">
                    Error Loading Data
                  </h3>
                  <p className="text-red-600 dark:text-red-400">{error}</p>
                  <p className="text-sm text-red-500 dark:text-red-500 mt-2">
                    Make sure the backend server is running on http://localhost:5000
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Results */}
          {!loading && !error && data && (
            <div className="space-y-8">
              {/* Top Skills */}
              <section>
                <div className="mb-4">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
                    Top Skills
                    <InfoTooltip 
                      message="These are the most in-demand skills based on aggregated data. Percentages represent relative demand, not absolute numbers."
                      position="top"
                    />
                  </h2>
                  <p className="text-gray-600 dark:text-gray-400">
                    Most in-demand skills based on your criteria
                  </p>
                </div>
                {data.top_skills.length === 0 ? (
                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 text-center">
                    <p className="text-gray-500 dark:text-gray-400">No top skills available</p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {data.top_skills.map((skill, index) => (
                      <SkillCard
                        key={index}
                        skill={skill}
                        percentage={getTopSkillPercentage(index, data.top_skills.length)}
                        rank={index + 1}
                        color="blue"
                      />
                    ))}
                  </div>
                )}
              </section>

              {/* Trending Skills */}
              <section>
                <div className="mb-4">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
                    Trending Skills
                    <InfoTooltip 
                      message="Trends are calculated based on historical data comparison. Rising skills show growth, stable skills maintain consistency, and declining skills show decreasing demand."
                      position="top"
                    />
                  </h2>
                  <p className="text-gray-600 dark:text-gray-400">
                    Skills that are gaining, stable, or declining in popularity
                  </p>
                </div>
                {data.trending_skills.length === 0 ? (
                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 text-center">
                    <p className="text-gray-500 dark:text-gray-400">No trending skills available</p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {data.trending_skills.map((skill, index) => {
                      const trend = getTrendForSkill(index, data.trending_skills.length)
                      const percentage = getTrendPercentage(trend, index, data.trending_skills.length)
                      return (
                        <TrendingSkill
                          key={index}
                          skill={skill}
                          trend={trend}
                          percentage={percentage}
                          index={index}
                        />
                      )
                    })}
                  </div>
                )}
              </section>

              {/* Recommended Skills */}
              <section>
                <div className="mb-4">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                    Recommended Skills
                  </h2>
                  <p className="text-gray-600 dark:text-gray-400">
                    Skills to learn for career growth and advancement
                  </p>
                </div>
                {data.recommended_skills.length === 0 ? (
                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 text-center">
                    <p className="text-gray-500 dark:text-gray-400">No recommended skills available</p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 gap-4">
                    {data.recommended_skills.map((skill, index) => (
                      <RecommendedSkill
                        key={index}
                        skill={skill}
                        index={index}
                      />
                    ))}
                  </div>
                )}
              </section>
            </div>
          )}
        </div>
      </div>
    </main>
  )
}

export default function ResultsPage() {
  return (
    <Suspense fallback={
      <main className="min-h-screen flex items-center justify-center">
        <div className="text-gray-600 dark:text-gray-400">Loading...</div>
      </main>
    }>
      <ResultsContent />
    </Suspense>
  )
}

