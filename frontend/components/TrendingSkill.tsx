'use client'

import { LineChart, Line, ResponsiveContainer, AreaChart, Area } from 'recharts'

interface TrendingSkillProps {
  skill: string
  trend: 'rising' | 'stable' | 'declining'
  percentage?: number
  index: number
}

export default function TrendingSkill({ skill, trend, percentage, index }: TrendingSkillProps) {
  // Generate trend data points based on trend type
  const generateTrendData = () => {
    const dataPoints = 6
    const data = []
    const now = new Date()
    
    for (let i = dataPoints - 1; i >= 0; i--) {
      const date = new Date(now)
      date.setMonth(date.getMonth() - i)
      
      let value: number
      if (trend === 'rising') {
        // Rising: start low and increase
        const baseValue = 30 + (index * 5)
        value = baseValue + ((dataPoints - i - 1) * 8) + Math.random() * 5
      } else if (trend === 'declining') {
        // Declining: start high and decrease
        const baseValue = 70 - (index * 5)
        value = baseValue - ((dataPoints - i - 1) * 6) - Math.random() * 5
      } else {
        // Stable: fluctuate around a median
        const baseValue = 50 + (index * 3)
        value = baseValue + (Math.random() * 10 - 5)
      }
      
      data.push({
        month: date.toLocaleDateString('en-US', { month: 'short' }),
        value: Math.max(0, Math.min(100, Math.round(value)))
      })
    }
    
    return data
  }

  const trendData = generateTrendData()
  
  const trendConfig = {
    rising: {
      bg: 'bg-green-50 dark:bg-green-900/20',
      border: 'border-green-200 dark:border-green-800',
      text: 'text-green-700 dark:text-green-300',
      chartColor: '#10b981', // green-500
      areaGradient: 'url(#greenGradient)',
      label: 'Rising',
      icon: '📈'
    },
    stable: {
      bg: 'bg-blue-50 dark:bg-blue-900/20',
      border: 'border-blue-200 dark:border-blue-800',
      text: 'text-blue-700 dark:text-blue-300',
      chartColor: '#3b82f6', // blue-500
      areaGradient: 'url(#blueGradient)',
      label: 'Stable',
      icon: '➡️'
    },
    declining: {
      bg: 'bg-orange-50 dark:bg-orange-900/20',
      border: 'border-orange-200 dark:border-orange-800',
      text: 'text-orange-700 dark:text-orange-300',
      chartColor: '#f97316', // orange-500
      areaGradient: 'url(#orangeGradient)',
      label: 'Declining',
      icon: '📉'
    }
  }

  const config = trendConfig[trend]
  const currentValue = trendData[trendData.length - 1]?.value || percentage || 0
  const previousValue = trendData[trendData.length - 2]?.value || currentValue
  const changePercent = previousValue > 0 
    ? Math.round(((currentValue - previousValue) / previousValue) * 100) 
    : 0

  return (
    <div className={`p-6 rounded-xl border-2 ${config.bg} ${config.border} transition-all hover:shadow-lg hover:scale-[1.02]`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="w-10 h-10 bg-gray-700 dark:bg-gray-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
            {index + 1}
          </span>
          <div>
            <span className={`font-semibold text-lg ${config.text} block`}>{skill}</span>
            <span className={`text-xs ${config.text} opacity-75 flex items-center gap-1`}>
              <span>{config.icon}</span>
              {config.label}
            </span>
          </div>
        </div>
        <div className="text-right">
          <div className={`text-2xl font-bold ${config.text}`}>{currentValue}%</div>
          {changePercent !== 0 && (
            <div className={`text-xs ${changePercent > 0 ? 'text-green-600' : 'text-orange-600'}`}>
              {changePercent > 0 ? '↑' : '↓'} {Math.abs(changePercent)}%
            </div>
          )}
        </div>
      </div>

      {/* Chart */}
      <div className="h-24 w-full -mx-2">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={trendData}>
            <defs>
              <linearGradient id="greenGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="blueGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="orangeGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#f97316" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#f97316" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <Area
              type="monotone"
              dataKey="value"
              stroke={config.chartColor}
              strokeWidth={2}
              fill={config.areaGradient}
              dot={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Timeline labels */}
      <div className="flex justify-between mt-2 text-xs text-gray-500 dark:text-gray-400">
        <span>{trendData[0]?.month}</span>
        <span>{trendData[Math.floor(trendData.length / 2)]?.month}</span>
        <span>{trendData[trendData.length - 1]?.month}</span>
      </div>
    </div>
  )
}
