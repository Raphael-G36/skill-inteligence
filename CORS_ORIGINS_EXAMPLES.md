# CORS_ORIGINS Configuration Examples

## What is CORS_ORIGINS?

`CORS_ORIGINS` tells your backend which frontend domains are allowed to make API requests. It's a security feature that prevents unauthorized websites from accessing your API.

## Format

- **Single domain**: `https://your-frontend.com`
- **Multiple domains**: `https://your-frontend.com,https://www.your-frontend.com`
- **With port (development)**: `http://localhost:3000`

## Examples by Deployment Scenario

### Scenario 1: Frontend on Vercel, Backend on Heroku

**Frontend URL**: `https://skill-intelligence.vercel.app`  
**Backend CORS_ORIGINS**:

```env
CORS_ORIGINS=https://skill-intelligence.vercel.app
```

If you have both www and non-www:

```env
CORS_ORIGINS=https://skill-intelligence.vercel.app,https://www.skill-intelligence.vercel.app
```

### Scenario 2: Frontend on Netlify, Backend on AWS

**Frontend URL**: `https://skill-intelligence.netlify.app`  
**Backend CORS_ORIGINS**:

```env
CORS_ORIGINS=https://skill-intelligence.netlify.app
```

### Scenario 3: Custom Domain

**Frontend URL**: `https://skillintelligence.com`  
**Backend CORS_ORIGINS**:

```env
CORS_ORIGINS=https://skillintelligence.com,https://www.skillintelligence.com
```

### Scenario 4: Frontend and Backend on Same Domain (Subdomain)

**Frontend**: `https://app.skillintelligence.com`  
**Backend**: `https://api.skillintelligence.com`  
**Backend CORS_ORIGINS**:

```env
CORS_ORIGINS=https://app.skillintelligence.com
```

### Scenario 5: Multiple Environments (Production + Staging)

**Production Frontend**: `https://skillintelligence.com`  
**Staging Frontend**: `https://staging.skillintelligence.com`  
**Backend CORS_ORIGINS**:

```env
CORS_ORIGINS=https://skillintelligence.com,https://www.skillintelligence.com,https://staging.skillintelligence.com
```

### Scenario 6: Local Development

**Frontend**: `http://localhost:3000`  
**Backend CORS_ORIGINS**:

```env
CORS_ORIGINS=http://localhost:3000
```

Or allow both localhost and production:

```env
CORS_ORIGINS=http://localhost:3000,https://skillintelligence.com
```

## How to Find Your Frontend URL

### If Using Vercel:

1. Go to your Vercel dashboard
2. Select your project
3. Check the "Domains" section
4. Use the production domain (e.g., `https://your-app.vercel.app`)

### If Using Netlify:

1. Go to your Netlify dashboard
2. Select your site
3. Check "Domain settings"
4. Use the production domain (e.g., `https://your-app.netlify.app`)

### If Using Custom Domain:

1. Check your DNS settings
2. Use the exact domain where your frontend is accessible
3. Include both `www` and non-`www` versions if both work

### If Using Other Platforms:

- Check your hosting platform's dashboard for the deployed URL
- It's usually in "Settings" > "Domains" or "Deployment" section

## Important Notes

### ✅ DO:

- Use **HTTPS** in production (not HTTP)
- Include **both www and non-www** if your site supports both
- Include **staging/preview URLs** if you need them
- Use **exact URLs** (include `https://` and no trailing slash)

### ❌ DON'T:

- Use `*` in production (security risk)
- Use `http://` in production (use HTTPS)
- Include trailing slashes (e.g., `https://example.com/`)
- Include paths (e.g., `https://example.com/app` - just the domain)

## Quick Checklist

Before setting `CORS_ORIGINS`, answer:

1. ✅ What is your frontend's production URL?
2. ✅ Does your site work with both `www` and non-`www`?
3. ✅ Do you have staging/preview environments that need access?
4. ✅ Are you using HTTPS in production?

## Example: Complete Setup

**Frontend**: Deployed to `https://skill-intelligence.vercel.app`  
**Backend**: Deployed to `https://skill-intelligence-api.herokuapp.com`

**Backend Environment Variables**:

```bash
SECRET_KEY=<your-secret-key>
FLASK_ENV=production
CORS_ORIGINS=https://skill-intelligence.vercel.app
PORT=5000
```

**Frontend Environment Variables**:

```bash
NEXT_PUBLIC_API_BASE_URL=https://skill-intelligence-api.herokuapp.com/api
```

## Testing CORS

After setting `CORS_ORIGINS`, test it:

1. Open your frontend in a browser
2. Open Developer Console (F12)
3. Try making an API request
4. Check for CORS errors in the console
5. If you see CORS errors, verify:
   - The frontend URL matches exactly what's in `CORS_ORIGINS`
   - You're using HTTPS (not HTTP) in production
   - No trailing slashes or paths in the URL

## Troubleshooting

**Error**: "Access to fetch blocked by CORS policy"

**Solutions**:

1. Check that your frontend URL exactly matches `CORS_ORIGINS`
2. Ensure you're using HTTPS in production
3. Verify no trailing slashes or extra paths
4. Restart your backend after changing `CORS_ORIGINS`
5. Check browser console for the exact origin being blocked
