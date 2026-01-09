# Environment Variables Setup

## Backend Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

```env
# Flask Configuration
FLASK_ENV=production
PORT=5000

# Security (REQUIRED in production)
SECRET_KEY=your-very-secure-secret-key-here-generate-with-python-secrets-token_hex

# Gunicorn Configuration (Production)
GUNICORN_WORKERS=4
GUNICORN_ACCESS_LOG=-
GUNICORN_ERROR_LOG=-
GUNICORN_LOG_LEVEL=info

# CORS Configuration (comma-separated origins, or * for all)
# Development: Use * to allow all origins (convenient for local testing)
# Production: MUST specify actual frontend domain(s) for security
# Examples:
#   Development: CORS_ORIGINS=*
#   Production: CORS_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com
#   Local dev with frontend on port 3000: CORS_ORIGINS=http://localhost:3000
CORS_ORIGINS=*

# API Configuration
API_TIMEOUT=30
```

## Generating a Secure SECRET_KEY

Run this Python command to generate a secure secret key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and use it as your `SECRET_KEY`.

## Frontend Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```env
# API Configuration
# Development:
NEXT_PUBLIC_API_BASE_URL=http://localhost:5000/api

# Production:
# NEXT_PUBLIC_API_BASE_URL=https://your-api-domain.com/api
```

**Important:** Only variables prefixed with `NEXT_PUBLIC_` are exposed to the browser in Next.js.

## Verifying Environment Variables

### Backend
Check if environment variables are loaded:
```bash
cd backend
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('SECRET_KEY:', 'SET' if os.getenv('SECRET_KEY') else 'NOT SET')"
```

### Frontend
Check if environment variable is available:
```bash
cd frontend
npm run build
# Check build output for any environment variable warnings
```

## Production Checklist

- [ ] `SECRET_KEY` is set and is a secure random string
- [ ] `FLASK_ENV` is set to `production`
- [ ] `CORS_ORIGINS` is set to actual frontend domain (not `*`)
- [ ] `NEXT_PUBLIC_API_BASE_URL` points to production backend URL
- [ ] `.env` files are in `.gitignore` (already configured)
- [ ] Environment variables are set in your hosting platform

