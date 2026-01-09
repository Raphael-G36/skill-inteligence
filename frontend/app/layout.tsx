import type { Metadata } from 'next'
import './globals.css'
import BannerWrapper from '@/components/BannerWrapper'

export const metadata: Metadata = {
  title: 'Skill Intelligence',
  description: 'Analyze and discover skills trends for your role and industry',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
        <BannerWrapper />
        {children}
      </body>
    </html>
  )
}

