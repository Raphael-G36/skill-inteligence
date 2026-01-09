'use client'

import { RadialBarChart, RadialBar, ResponsiveContainer, Cell } from 'recharts'

interface RecommendedSkillProps {
  skill: string
  index: number
}

export default function RecommendedSkill({ skill, index }: RecommendedSkillProps) {
  // Generate recommendation score (higher for earlier items)
  const recommendationScore = Math.round(90 - (index * 8) + Math.random() * 10)
  
  // Create data for radial chart
  const chartData = [
    { name: 'Match', value: recommendationScore, fill: '#8b5cf6' }
  ]

  // Different colors for variety
  const colors = [
    { gradient: 'from-purple-500 to-pink-500', fill: '#8b5cf6' },
    { gradient: 'from-blue-500 to-cyan-500', fill: '#3b82f6' },
    { gradient: 'from-indigo-500 to-purple-500', fill: '#6366f1' },
    { gradient: 'from-pink-500 to-rose-500', fill: '#ec4899' },
    { gradient: 'from-violet-500 to-purple-500', fill: '#8b5cf6' }
  ]

  const colorScheme = colors[index % colors.length]

  return (
    <div className="p-6 rounded-xl border-2 bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 border-purple-200 dark:border-purple-800 transition-all hover:shadow-lg hover:scale-[1.01]">
      <div className="flex items-center gap-6">
        {/* Radial Chart */}
        <div className="flex-shrink-0">
          <div className="w-24 h-24 relative">
            <ResponsiveContainer width="100%" height="100%">
              <RadialBarChart
                innerRadius="70%"
                outerRadius="100%"
                data={chartData}
                startAngle={90}
                endAngle={-270}
              >
                <RadialBar
                  dataKey="value"
                  cornerRadius={8}
                  fill={colorScheme.fill}
                  opacity={0.9}
                />
                <Cell fill="#e5e7eb" opacity={0.2} />
              </RadialBarChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-700 dark:text-purple-300">
                  {recommendationScore}
                </div>
                <div className="text-xs text-purple-600 dark:text-purple-400">%</div>
              </div>
            </div>
          </div>
        </div>

        {/* Skill Info */}
        <div className="flex-1">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-xl font-bold text-purple-900 dark:text-purple-100">
              {skill}
            </h3>
            <span className="px-3 py-1 bg-purple-200 dark:bg-purple-800 text-purple-700 dark:text-purple-300 text-xs font-semibold rounded-full">
              Recommended
            </span>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
            High growth potential • Trending technology • Career advancement
          </p>
          
          {/* Recommendation badges */}
          <div className="flex flex-wrap gap-2">
            <span className="px-2 py-1 bg-white/50 dark:bg-gray-800/50 text-purple-700 dark:text-purple-300 text-xs rounded-md border border-purple-200 dark:border-purple-700">
              ⭐ High Demand
            </span>
            <span className="px-2 py-1 bg-white/50 dark:bg-gray-800/50 text-purple-700 dark:text-purple-300 text-xs rounded-md border border-purple-200 dark:border-purple-700">
              📈 Growing
            </span>
            <span className="px-2 py-1 bg-white/50 dark:bg-gray-800/50 text-purple-700 dark:text-purple-300 text-xs rounded-md border border-purple-200 dark:border-purple-700">
              💼 Career Growth
            </span>
          </div>
        </div>

        {/* Arrow indicator */}
        <div className="flex-shrink-0">
          <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center shadow-lg">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </div>
        </div>
      </div>
    </div>
  )
}
