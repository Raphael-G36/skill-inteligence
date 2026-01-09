'use client'

import { useState, useEffect } from 'react'

interface PrototypeBannerProps {
  message?: string
  storageKey?: string
}

export default function PrototypeBanner({ 
  message = "⚠️ Prototype: This tool is an MVP. Some features are limited. Results may not cover every role or industry.",
  storageKey = 'prototype-banner-dismissed'
}: PrototypeBannerProps) {
  const [isDismissed, setIsDismissed] = useState(true)

  useEffect(() => {
    // Check if banner was previously dismissed
    const dismissed = localStorage.getItem(storageKey)
    setIsDismissed(dismissed === 'true')
  }, [storageKey])

  const handleDismiss = () => {
    setIsDismissed(true)
    localStorage.setItem(storageKey, 'true')
  }

  if (isDismissed) {
    return null
  }

  return (
    <div className="bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-900/20 dark:to-orange-900/20 border-b border-amber-200 dark:border-amber-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between py-3">
          <div className="flex items-center gap-3 flex-1">
            <div className="flex-shrink-0">
              <svg 
                className="w-5 h-5 text-amber-600 dark:text-amber-400" 
                fill="currentColor" 
                viewBox="0 0 20 20"
              >
                <path 
                  fillRule="evenodd" 
                  d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" 
                  clipRule="evenodd" 
                />
              </svg>
            </div>
            <p className="text-sm font-medium text-amber-800 dark:text-amber-200 flex-1">
              {message}
            </p>
          </div>
          <button
            onClick={handleDismiss}
            className="ml-4 flex-shrink-0 p-1.5 rounded-md text-amber-600 dark:text-amber-400 hover:bg-amber-100 dark:hover:bg-amber-900/30 transition-colors focus:outline-none focus:ring-2 focus:ring-amber-500"
            aria-label="Dismiss banner"
          >
            <svg 
              className="w-5 h-5" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M6 18L18 6M6 6l12 12" 
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  )
}

