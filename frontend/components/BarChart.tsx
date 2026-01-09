interface BarChartProps {
  data: Array<{ label: string; value: number }>
  title: string
  maxValue?: number
  color?: 'blue' | 'green' | 'purple'
}

export default function BarChart({ data, title, maxValue, color = 'blue' }: BarChartProps) {
  const colorClasses = {
    blue: 'bg-blue-600 dark:bg-blue-500',
    green: 'bg-green-600 dark:bg-green-500',
    purple: 'bg-purple-600 dark:bg-purple-500'
  }
  
  const barColor = colorClasses[color]
  // Calculate max value if not provided
  const max = maxValue || (data.length > 0 ? Math.max(...data.map(item => item.value)) : 1)

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">{title}</h3>
      <div className="space-y-3">
        {data.length === 0 ? (
          <p className="text-gray-500 dark:text-gray-400 text-center py-4">No data available</p>
        ) : (
          data.map((item, index) => (
            <div key={index} className="space-y-1">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  {item.label}
                </span>
                <span className="text-sm text-gray-600 dark:text-gray-400">{item.value}</span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-6 overflow-hidden">
                <div
                  className={`${barColor} h-6 rounded-full transition-all duration-500 ease-out flex items-center justify-end pr-2`}
                  style={{ width: `${(item.value / max) * 100}%` }}
                >
                  {item.value > 0 && (
                    <span className="text-xs font-medium text-white">
                      {Math.round((item.value / max) * 100)}%
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

