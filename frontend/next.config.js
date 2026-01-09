const path = require('path')
const fs = require('fs')

// #region agent log
const LOG_PATH = path.join(__dirname, '..', '.cursor', 'debug.log')
const log = (data) => {
  try {
    const logEntry = JSON.stringify({...data, timestamp: Date.now()}) + '\n'
    fs.appendFileSync(LOG_PATH, logEntry)
  } catch (e) {}
}

// Log initial config load
log({
  sessionId: 'debug-session',
  runId: 'build',
  hypothesisId: 'B',
  location: 'next.config.js:init',
  message: 'Config file loaded',
  data: {
    __dirname,
    cwd: process.cwd(),
    tsconfigPath: path.join(__dirname, 'tsconfig.json'),
    tsconfigExists: fs.existsSync(path.join(__dirname, 'tsconfig.json'))
  }
})

// Read and log tsconfig
try {
  const tsconfigPath = path.join(__dirname, 'tsconfig.json')
  if (fs.existsSync(tsconfigPath)) {
    const tsconfig = JSON.parse(fs.readFileSync(tsconfigPath, 'utf8'))
    log({
      sessionId: 'debug-session',
      runId: 'build',
      hypothesisId: 'B',
      location: 'next.config.js:init',
      message: 'tsconfig.json read',
      data: {
        baseUrl: tsconfig.compilerOptions?.baseUrl,
        paths: tsconfig.compilerOptions?.paths
      }
    })
  }
} catch (e) {
  log({
    sessionId: 'debug-session',
    runId: 'build',
    hypothesisId: 'B',
    location: 'next.config.js:init',
    message: 'tsconfig read error',
    data: { error: e.message }
  })
}
// #endregion

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  
  // Production optimizations
  compress: true,
  poweredByHeader: false,
  
  // Image optimization
  images: {
    formats: ['image/avif', 'image/webp'],
    minimumCacheTTL: 60,
  },
  
  // Output configuration
  output: 'standalone', // For Docker deployments
  
  // Webpack configuration for path aliases
  webpack: (config, { isServer }) => {
    // #region agent log
    const resolvedAlias = path.resolve(__dirname)
    const apiPath = path.join(resolvedAlias, 'lib', 'api.ts')
    const apiPathJs = path.join(resolvedAlias, 'lib', 'api.js')
    const apiExists = fs.existsSync(apiPath) || fs.existsSync(apiPathJs)
    
    // Check multiple possible locations
    const libDir = path.join(resolvedAlias, 'lib')
    const libExists = fs.existsSync(libDir)
    const libContents = libExists ? fs.readdirSync(libDir) : []
    
    log({
      sessionId: 'debug-session',
      runId: 'build',
      hypothesisId: 'A',
      location: 'next.config.js:webpack',
      message: 'Webpack config - path resolution',
      data: {
        __dirname,
        resolvedAlias,
        apiPath,
        apiPathJs,
        apiExists,
        libDir,
        libExists,
        libContents,
        isServer,
        existingAliases: Object.keys(config.resolve.alias || {}),
        resolveModules: config.resolve.modules || []
      }
    })
    // #endregion
    
    // Apply alias - ensure we don't override Next.js defaults
    const existingAliases = config.resolve.alias || {}
    config.resolve.alias = {
      ...existingAliases,
      '@': resolvedAlias,
    }
    
    // Also add to resolve.modules if needed
    if (!config.resolve.modules) {
      config.resolve.modules = ['node_modules']
    }
    
    // #region agent log
    log({
      sessionId: 'debug-session',
      runId: 'build',
      hypothesisId: 'A',
      location: 'next.config.js:webpack',
      message: 'Webpack config - alias applied',
      data: {
        finalAlias: config.resolve.alias['@'],
        allAliases: Object.keys(config.resolve.alias),
        modules: config.resolve.modules
      }
    })
    // #endregion
    
    return config
  },
  
  // Environment variables
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:5000/api',
  },
  
  // Headers for security
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on'
          },
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block'
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin'
          },
        ],
      },
    ]
  },
}

module.exports = nextConfig

