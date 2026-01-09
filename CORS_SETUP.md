# CORS Configuration Guide

## Overview

CORS (Cross-Origin Resource Sharing) is properly configured to allow the Next.js frontend (port 3000) to communicate with the Flask backend (port 5000).

## Configuration

### Backend CORS Setup

CORS is enabled globally in `backend/app/__init__.py` using Flask-CORS.

**Development Mode (Default):**
```python
# Allows all origins - convenient for local development
CORS_ORIGINS=*
```

**Production Mode:**
```python
# Restrict to specific frontend domain(s)
CORS_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com
```

### Environment Variable

Set `CORS_ORIGINS` in your `.env` file:

```env
# Development - allow all origins
CORS_ORIGINS=*

# Production - specific domains only
CORS_ORIGINS=https://skill-intelligence.com,https://www.skill-intelligence.com

# Local development with specific port
CORS_ORIGINS=http://localhost:3000
```

## How It Works

1. **Global CORS Configuration**: CORS is enabled globally for the entire Flask application
2. **Automatic OPTIONS Handling**: Flask-CORS automatically handles OPTIONS preflight requests
3. **All Routes Protected**: All API endpoints (`/api/*`) and health check (`/health`) have CORS enabled
4. **Explicit Decorators**: Each route also has `@cross_origin()` decorator for clarity (redundant but explicit)

## CORS Headers Sent

When CORS is enabled, the backend automatically sends these headers:

```
Access-Control-Allow-Origin: <origin-or-*>
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
Access-Control-Max-Age: 3600
```

## Testing CORS

### Test from Browser Console

```javascript
// Test from frontend (http://localhost:3000)
fetch('http://localhost:5000/api/', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(data => console.log('CORS working!', data))
.catch(error => console.error('CORS error:', error));
```

### Test with curl

```bash
# Test OPTIONS preflight request
curl -X OPTIONS http://localhost:5000/api/analyze \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v

# Should return 200 with CORS headers
```

### Test POST Request

```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Origin: http://localhost:3000" \
  -H "Content-Type: application/json" \
  -d '{"role":"Backend Engineer","industry":"FinTech","region":"Global"}' \
  -v
```

## Troubleshooting

### CORS Error: "Access to fetch blocked by CORS policy"

**Cause:** Backend is not allowing the frontend origin.

**Solutions:**
1. Check `CORS_ORIGINS` in backend `.env` file
2. Ensure it includes your frontend URL (e.g., `http://localhost:3000`)
3. Restart the backend server after changing `.env`
4. Verify the frontend is using the correct API base URL

### CORS Error: "Preflight request failed"

**Cause:** OPTIONS request is not being handled correctly.

**Solutions:**
1. Verify Flask-CORS is installed: `pip install Flask-CORS`
2. Check that CORS is enabled in `app/__init__.py`
3. Ensure the backend is running and accessible

### CORS Works in Development but Fails in Production

**Cause:** Production environment has different origin restrictions.

**Solutions:**
1. Set `CORS_ORIGINS` to your production frontend domain
2. Don't use `*` in production (security risk)
3. Use HTTPS URLs for production
4. Restart backend after changing environment variables

## Security Best Practices

### Development
- ✅ `CORS_ORIGINS=*` is acceptable for local development
- ✅ Makes testing easier across different ports

### Production
- ❌ **NEVER use `CORS_ORIGINS=*` in production**
- ✅ Always specify exact frontend domain(s)
- ✅ Use HTTPS URLs only
- ✅ Include both www and non-www versions if applicable
- ✅ Example: `CORS_ORIGINS=https://skill-intelligence.com,https://www.skill-intelligence.com`

## Verification Checklist

- [ ] Backend starts without CORS errors
- [ ] Frontend can make GET requests to `/api/`
- [ ] Frontend can make POST requests to `/api/analyze`
- [ ] OPTIONS preflight requests return 200 OK
- [ ] CORS headers are present in API responses
- [ ] Production CORS_ORIGINS is set to specific domain (not `*`)

## Additional Notes

- CORS is configured to **not** support credentials (`supports_credentials=False`)
- Only `Content-Type` header is allowed (sufficient for this API)
- All API endpoints have CORS enabled automatically
- Health check endpoint (`/health`) also has CORS enabled

## Related Files

- `backend/app/__init__.py` - Global CORS configuration
- `backend/app/config.py` - CORS_ORIGINS environment variable handling
- `backend/app/routes/api.py` - API endpoints with explicit CORS decorators
- `backend/app/routes/health.py` - Health check with CORS
- `backend/requirements.txt` - Flask-CORS dependency

