# Environment Variables: Development vs Production

## How It Works

Your code uses `python-dotenv` with `load_dotenv()`, which means it supports **both** methods:

1. **Development (Local)**: Uses `.env` file (convenient for local development)
2. **Production (Deployment)**: Uses **actual environment variables** set in your hosting platform

The `load_dotenv()` function will:
- First try to load from `.env` file (if it exists)
- If `.env` doesn't exist, it falls back to actual environment variables from the system
- This means it works seamlessly in both environments

## Development Setup (Local)

**Use `.env` file** - Create `backend/.env`:

```env
FLASK_ENV=development
PORT=5000
SECRET_KEY=dev-secret-key-change-in-production
CORS_ORIGINS=*
API_TIMEOUT=30
```

✅ **Pros**: Easy to manage, all variables in one file
✅ **Cons**: File must exist, but that's fine for development

## Production Deployment

**❌ DO NOT use `.env` file in production**

**✅ DO set environment variables through your hosting platform**

### Why Not `.env` in Production?

1. **Security Risk**: `.env` files can accidentally be committed to git (even though they're in `.gitignore`)
2. **Not Standard Practice**: Production hosting platforms expect environment variables
3. **Scalability**: Environment variables are easier to manage across multiple servers
4. **Compliance**: Better for security audits and compliance

### How to Set Environment Variables in Production

#### Option 1: Heroku
```bash
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set FLASK_ENV=production
heroku config:set CORS_ORIGINS=https://your-frontend.com
heroku config:set PORT=5000
```

#### Option 2: AWS (Elastic Beanstalk / EC2)
```bash
# Via AWS Console: EC2 > Configuration > Environment Variables
# Or via EB CLI:
eb setenv SECRET_KEY=your-secret-key FLASK_ENV=production CORS_ORIGINS=https://your-frontend.com
```

#### Option 3: DigitalOcean App Platform
```yaml
# In app.yaml or via Console > App Settings > Environment Variables
envs:
  - key: SECRET_KEY
    value: your-secret-key
    scope: RUN_TIME
  - key: FLASK_ENV
    value: production
    scope: RUN_TIME
  - key: CORS_ORIGINS
    value: https://your-frontend.com
    scope: RUN_TIME
```

#### Option 4: Docker
```dockerfile
# In Dockerfile or docker-compose.yml
ENV SECRET_KEY=your-secret-key
ENV FLASK_ENV=production
ENV CORS_ORIGINS=https://your-frontend.com

# Or via docker run:
docker run -e SECRET_KEY=your-secret-key -e FLASK_ENV=production your-image
```

#### Option 5: VPS (DigitalOcean Droplet, Linode, etc.)
```bash
# In ~/.bashrc or ~/.profile, or systemd service file:
export SECRET_KEY=your-secret-key
export FLASK_ENV=production
export CORS_ORIGINS=https://your-frontend.com

# Or use systemd service file:
[Service]
Environment="SECRET_KEY=your-secret-key"
Environment="FLASK_ENV=production"
Environment="CORS_ORIGINS=https://your-frontend.com"
```

## Required Environment Variables for Production

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | ✅ **YES** | None | Strong secret key (generate with `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `FLASK_ENV` | ✅ **YES** | `development` | Must be `production` |
| `CORS_ORIGINS` | ✅ **YES** | `*` | Comma-separated list of frontend domains (e.g., `https://app.example.com,https://www.app.example.com`) |
| `PORT` | ⚠️ Optional | `5000` | Port number (often set by hosting platform) |
| `API_TIMEOUT` | ⚠️ Optional | `30` | API timeout in seconds |
| `GUNICORN_WORKERS` | ⚠️ Optional | Auto | Number of worker processes |
| `GUNICORN_LOG_LEVEL` | ⚠️ Optional | `info` | Logging level |

## Verification

### Check Environment Variables in Production

```bash
# SSH into your server and run:
python -c "import os; print('SECRET_KEY:', 'SET' if os.getenv('SECRET_KEY') else 'NOT SET'); print('FLASK_ENV:', os.getenv('FLASK_ENV', 'NOT SET'))"
```

### Test Locally Without .env File

To test how it works in production (without .env file):

```bash
# Set environment variables directly
export SECRET_KEY=test-secret-key
export FLASK_ENV=production
export CORS_ORIGINS=https://example.com

# Remove or rename .env temporarily
mv backend/.env backend/.env.backup

# Run the app - it should use environment variables
cd backend
python run.py

# Restore .env after testing
mv backend/.env.backup backend/.env
```

## Best Practices

### ✅ DO:
- Use `.env` files for **local development only**
- Set environment variables through your **hosting platform** in production
- Never commit `.env` files to git (already in `.gitignore`)
- Use strong, randomly generated `SECRET_KEY` in production
- Set `CORS_ORIGINS` to specific domains (not `*`) in production
- Set `FLASK_ENV=production` in production

### ❌ DON'T:
- Commit `.env` files to git
- Use `.env` files in production deployments
- Use `*` for `CORS_ORIGINS` in production
- Use weak or default `SECRET_KEY` in production
- Hardcode secrets in your code

## Summary

**Your current code is already set up correctly!** 

- `load_dotenv()` loads from `.env` if it exists (for development)
- Falls back to environment variables if `.env` doesn't exist (for production)
- This is the **best practice** approach

**For deployment:**
1. ✅ Set environment variables in your hosting platform
2. ❌ Do NOT upload `.env` file to production
3. ✅ The code will automatically use environment variables

Your code already handles both scenarios seamlessly! 🎉

