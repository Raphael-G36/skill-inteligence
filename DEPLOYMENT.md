# Deployment Guide

This guide covers deploying the Skill Intelligence application to production.

## Backend Deployment

### Prerequisites

- Python 3.9 or higher
- pip
- Virtual environment (recommended)

### Setup Steps

1. **Create virtual environment:**

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**

   ⚠️ **Important**: For production, set environment variables through your hosting platform, NOT via `.env` file.

   **DO NOT** upload `.env` files to production servers. Instead, set environment variables through:

   - Heroku: `heroku config:set KEY=value`
   - AWS: Console or `eb setenv KEY=value`
   - DigitalOcean: App Platform settings or `doctl apps create`
   - Docker: `-e` flags or `docker-compose.yml`
   - VPS: System environment variables or systemd service file

   See [ENV_DEPLOYMENT_GUIDE.md](./ENV_DEPLOYMENT_GUIDE.md) for detailed instructions.

   **Required environment variables for production:**

   - `SECRET_KEY`: Generate a strong secret key (required)
   - `FLASK_ENV`: Must be set to `production`
   - `CORS_ORIGINS`: Comma-separated list of allowed origins (required, not `*`)
   - `PORT`: Port number (optional, often set by hosting platform)

4. **Run with Gunicorn (Production):**

   ```bash
   gunicorn -c gunicorn.conf.py wsgi:app
   ```

   Or with custom settings:

   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 --timeout 30 wsgi:app
   ```

5. **Run in development mode:**
   ```bash
   python run.py
   ```

### Gunicorn Configuration

The `gunicorn.conf.py` file contains production-ready settings:

- **Workers**: Automatically set based on CPU count (2 \* CPU + 1)
- **Timeout**: 30 seconds
- **Logging**: Configurable via environment variables
- **Binding**: Listens on 0.0.0.0 (all interfaces)

### Environment Variables Reference

| Variable             | Default       | Description                          |
| -------------------- | ------------- | ------------------------------------ |
| `FLASK_ENV`          | `development` | Environment (development/production) |
| `PORT`               | `5000`        | Port to bind to                      |
| `SECRET_KEY`         | (required)    | Secret key for Flask sessions        |
| `CORS_ORIGINS`       | `*`           | Comma-separated allowed origins      |
| `GUNICORN_WORKERS`   | `4`           | Number of worker processes           |
| `GUNICORN_LOG_LEVEL` | `info`        | Logging level                        |

## Frontend Deployment

### Prerequisites

- Node.js 18 or higher
- npm or yarn

### Setup Steps

1. **Install dependencies:**

   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment variables:**

   ⚠️ **Important**: For production, set environment variables through your hosting platform (Vercel, Netlify, etc.).

   **For local development**: Create `.env.local` file:

   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:5000/api
   ```

   **For production**: Set via hosting platform settings:

   ```env
   NEXT_PUBLIC_API_BASE_URL=https://your-api-domain.com/api
   ```

   **Note:**

   - Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser
   - Next.js embeds these at build time, so rebuild after changing them

3. **Build for production:**

   ```bash
   npm run build
   ```

4. **Start production server:**

   ```bash
   npm start
   ```

5. **Run development server:**
   ```bash
   npm run dev
   ```

### Production Build Features

The Next.js configuration includes:

- **Standalone output**: Optimized for Docker deployments
- **Security headers**: XSS protection, frame options, etc.
- **Image optimization**: AVIF and WebP support
- **Compression**: Gzip compression enabled
- **React Strict Mode**: Enabled for better development experience

### Environment Variables Reference

| Variable                   | Default                     | Description          |
| -------------------------- | --------------------------- | -------------------- |
| `NEXT_PUBLIC_API_BASE_URL` | `http://localhost:5000/api` | Backend API base URL |

## Docker Deployment (Optional)

### Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production
ENV PORT=5000

EXPOSE 5000

CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi:app"]
```

### Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:18-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

ENV PORT=3000

CMD ["node", "server.js"]
```

## Deployment Checklist

### Backend

- [ ] Set `FLASK_ENV=production`
- [ ] Generate and set strong `SECRET_KEY`
- [ ] Configure `CORS_ORIGINS` with actual frontend domain
- [ ] Set appropriate `GUNICORN_WORKERS` based on server capacity
- [ ] Configure logging (access/error logs)
- [ ] Test health endpoint: `GET /health`

### Frontend

- [ ] Set `NEXT_PUBLIC_API_BASE_URL` to production backend URL
- [ ] Run `npm run build` successfully
- [ ] Test production build locally with `npm start`
- [ ] Verify all API calls work correctly
- [ ] Check that environment variables are loaded

### CORS Configuration

- [ ] **CORS is properly configured** - Backend allows requests from frontend
- [ ] Development: `CORS_ORIGINS=*` (allows all origins for local testing)
- [ ] Production: `CORS_ORIGINS=https://your-frontend-domain.com` (specific domain only)
- [ ] Test frontend can successfully make API calls to backend
- [ ] Verify CORS headers are present in API responses:
  - `Access-Control-Allow-Origin` header should be present
  - `Access-Control-Allow-Methods` should include GET, POST, OPTIONS
  - `Access-Control-Allow-Headers` should include Content-Type

### Security

- [ ] Use HTTPS in production
- [ ] Set secure CORS origins (not `*` in production)
- [ ] Use strong SECRET_KEY
- [ ] Keep dependencies updated
- [ ] Review security headers
- [ ] Use environment variables for sensitive data

## Common Deployment Platforms

### Heroku

**Backend:**

```bash
heroku create skill-intelligence-api
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
heroku config:set CORS_ORIGINS=https://your-frontend.herokuapp.com
git push heroku main
```

**Frontend:**

```bash
heroku create skill-intelligence-frontend
heroku config:set NEXT_PUBLIC_API_BASE_URL=https://skill-intelligence-api.herokuapp.com/api
git push heroku main
```

### Vercel (Frontend)

1. Connect your GitHub repository
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push

### Railway / Render

Similar to Heroku, configure environment variables and deploy.

## Troubleshooting

### Backend Issues

**Port already in use:**

- Change `PORT` environment variable
- Or kill existing process on the port

**CORS errors:**

- Verify `CORS_ORIGINS` includes your frontend URL
- Check that frontend is using correct API base URL

**Gunicorn workers crashing:**

- Reduce `GUNICORN_WORKERS` count
- Check application logs for errors
- Increase timeout if needed

### Frontend Issues

**API calls failing:**

- Verify `NEXT_PUBLIC_API_BASE_URL` is set correctly
- Check CORS configuration on backend
- Verify backend is running and accessible

**Build errors:**

- Clear `.next` folder: `rm -rf .next`
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check for TypeScript errors: `npm run lint`

## Monitoring

### Health Checks

- Backend: `GET /health`
- Frontend: Root endpoint should return 200

### Logging

- Backend logs go to stdout/stderr (configure via Gunicorn)
- Frontend logs in browser console and server logs

## Support

For issues or questions, refer to:

- Flask documentation: https://flask.palletsprojects.com/
- Next.js documentation: https://nextjs.org/docs
- Gunicorn documentation: https://docs.gunicorn.org/
