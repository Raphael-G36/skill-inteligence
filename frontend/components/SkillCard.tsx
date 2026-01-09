'use client'

import { BarChart, Bar, ResponsiveContainer, Cell } from 'recharts'

interface SkillCardProps {
  skill: string
  percentage: number
  rank: number
  color?: 'blue' | 'green' | 'purple'
}

export default function SkillCard({ skill, percentage, rank, color = 'blue' }: SkillCardProps) {
  const colorClasses = {
    blue: {
      bg: 'bg-blue-50 dark:bg-blue-900/20',
      border: 'border-blue-200 dark:border-blue-800',
      text: 'text-blue-700 dark:text-blue-300',
      badge: 'bg-blue-600 text-white',
      bar: 'bg-blue-600',
      chartColor: '#2563eb'
    },
    green: {
      bg: 'bg-green-50 dark:bg-green-900/20',
      border: 'border-green-200 dark:border-green-800',
      text: 'text-green-700 dark:text-green-300',
      badge: 'bg-green-600 text-white',
      bar: 'bg-green-600',
      chartColor: '#16a34a'
    },
    purple: {
      bg: 'bg-purple-50 dark:bg-purple-900/20',
      border: 'border-purple-200 dark:border-purple-800',
      text: 'text-purple-700 dark:text-purple-300',
      badge: 'bg-purple-600 text-white',
      bar: 'bg-purple-600',
      chartColor: '#9333ea'
    }
  }

  const colors = colorClasses[color]
  
  // Create comparison data for the bar chart (showing this skill vs others)
  const chartData = [
    { name: 'Q1', value: Math.max(20, percentage - 15 + Math.random() * 10) },
    { name: 'Q2', value: Math.max(30, percentage - 10 + Math.random() * 10) },
    { name: 'Q3', value: Math.max(40, percentage - 5 + Math.random() * 10) },
    { name: 'Q4', value: percentage }
  ].map(item => ({
    ...item,
    value: Math.min(100, Math.round(item.value))
  }))

  return (
    <div className={`p-6 rounded-xl border-2 ${colors.bg} ${colors.border} transition-all hover:shadow-lg hover:scale-[1.02]`}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className={`${colors.badge} w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold shadow-md`}>
            {rank}
          </span>
          <span className={`font-semibold text-lg ${colors.text}`}>{skill}</span>
        </div>
        <div className="text-right">
          <span className={`text-3xl font-bold ${colors.text}`}>{percentage}%</span>
          <div className="text-xs text-gray-500 dark:text-gray-400">demand</div>
        </div>
      </div>

      {/* Mini Bar Chart showing quarterly trend */}
      <div className="h-20 w-full -mx-2 mb-2">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <Bar 
              dataKey="value" 
              radius={[4, 4, 0, 0]}
              fill={colors.chartColor}
            >
              {chartData.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={colors.chartColor}
                  opacity={0.7 + (index * 0.1)}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Progress bar */}
      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 overflow-hidden">
        <div
          className={`${colors.bar} h-2.5 rounded-full transition-all duration-500 ease-out shadow-sm`}
          style={{ width: `${percentage}%` }}
        />
      </div>

      {/* Quarter labels */}
      <div className="flex justify-between mt-2 text-xs text-gray-500 dark:text-gray-400">
        <span>Q1</span>
        <span>Q2</span>
        <span>Q3</span>
        <span>Q4</span>
      </div>
    </div>
  )
}
