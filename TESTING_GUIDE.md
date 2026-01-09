# Quick Testing Guide

This guide shows you how to test the Skill Intelligence application locally.

## Prerequisites Check

Verify you have the required tools:

```bash
# Check Python version (should be 3.9+)
python --version

# Check Node.js version (should be 18+)
node --version

# Check npm version
npm --version
```

## Quick Start Testing

### Step 1: Start the Backend Server

Open a terminal and run:

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (if not already done)
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Start the Flask server
python run.py
```

**Expected output:**

```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

The backend should now be running on `http://localhost:5000`

### Step 2: Test Backend Endpoints

Open a **new terminal** (keep backend running) and test the API:

#### Test Health Endpoint:

```bash
# Windows PowerShell:
Invoke-WebRequest -Uri http://localhost:5000/health -Method GET | Select-Object -ExpandProperty Content

# Windows CMD or macOS/Linux:
curl http://localhost:5000/health
```

**Expected response:**

```json
{
  "status": "ok",
  "message": "Skill Intelligence API is running",
  "service": "Skill Intelligence API"
}
```

#### Test Analyze Endpoint:

```bash
# Windows PowerShell:
$body = @{
    role = "Backend Engineer"
    industry = "FinTech"
    region = "Global"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:5000/api/analyze -Method POST -Body $body -ContentType "application/json" | Select-Object -ExpandProperty Content

# Windows CMD or macOS/Linux:
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d "{\"role\":\"Backend Engineer\",\"industry\":\"FinTech\",\"region\":\"Global\"}"
```

**Expected response:**

```json
{
  "top_skills": ["Python", "JavaScript", ...],
  "trending_skills": ["AI/ML Integration", ...],
  "recommended_skills": ["System Design", ...]
}
```

### Step 3: Start the Frontend Server

Open a **new terminal** (keep backend running) and run:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already installed)
npm install

# Start the Next.js development server
npm run dev
```

**Expected output:**

```
  ▲ Next.js 14.2.5
  - Local:        http://localhost:3000
  - Ready in 2.3s
```

The frontend should now be running on `http://localhost:3000`

### Step 4: Test in Browser

1. **Open your browser** and go to: `http://localhost:3000`

2. **Fill out the form:**

   - Role: `Backend Engineer`
   - Industry: `FinTech`
   - Region: Select `Global` from dropdown

3. **Click "Analyze Skills"**

4. **Expected behavior:**
   - Form submits and navigates to results page
   - Loading spinner appears
   - Results page displays:
     - Search criteria (role, industry, region)
     - Top Skills section with skill cards and percentages
     - Trending Skills section with trend arrows (↑ ↓ →)
     - Recommended Skills section with highlighted cards

### Step 5: Verify CORS is Working

Open browser **Developer Console** (F12) and check:

1. **Network tab:**

   - Look for request to `http://localhost:5000/api/analyze`
   - Status should be `200 OK`
   - Check Response Headers for CORS headers:
     - `Access-Control-Allow-Origin: http://localhost:3000` (or `*`)
     - `Access-Control-Allow-Methods: GET, POST, OPTIONS`

2. **Console tab:**
   - Should have no CORS errors
   - If you see CORS errors, check that backend is running and CORS_ORIGINS is set

### Step 6: Test Additional Endpoints (Optional)

#### Test Skill Extraction:

```bash
curl -X POST http://localhost:5000/api/extract-skills \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"I have experience with Python, PostgreSQL, React, and Docker. Also worked with Node.js.\"}"
```

#### Test Job Postings Ingestion:

```bash
curl -X POST http://localhost:5000/api/job-postings/ingest \
  -H "Content-Type: application/json" \
  -d "{\"use_mock\":true,\"role\":\"Backend Engineer\",\"industry\":\"FinTech\",\"count\":5}"
```

#### Test GitHub Ingestion:

```bash
curl -X POST http://localhost:5000/api/github/ingest \
  -H "Content-Type: application/json" \
  -d "{\"role\":\"Backend Engineer\",\"industry\":\"FinTech\",\"max_repos\":5}"
```

## Troubleshooting

### Backend won't start

**Error: "Port 5000 is already in use"**

```bash
# Windows: Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:5000 | xargs kill -9

# Or change port in .env:
PORT=5001
```

**Error: "Module not found"**

```bash
# Make sure you're in the backend directory and virtual environment is activated
cd backend
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**Error: "No module named 'app'"**

```bash
# Make sure you're running from the backend directory
cd backend
python run.py
```

### Frontend won't start

**Error: "Port 3000 is already in use"**

```bash
# Windows: Find and kill process
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:3000 | xargs kill -9

# Or change port:
npm run dev -- -p 3001
```

**Error: "Cannot find module"**

```bash
# Delete node_modules and reinstall
rm -rf node_modules
rm package-lock.json
npm install
```

### CORS Errors in Browser

**Error: "Access to fetch blocked by CORS policy"**

1. **Check backend is running:**

   ```bash
   curl http://localhost:5000/health
   ```

2. **Check CORS configuration:**

   - Verify `CORS_ORIGINS=*` in backend `.env` file (or leave default)
   - Restart backend after changing `.env`

3. **Check frontend API URL:**

   - Verify `NEXT_PUBLIC_API_BASE_URL=http://localhost:5000/api` in frontend `.env.local`
   - Restart frontend after changing `.env.local`

4. **Check browser console:**
   - Look for the actual error message
   - Verify the Origin header matches what backend expects

### API Returns Errors

**Error: "Request body is required"**

- Make sure you're sending JSON with `Content-Type: application/json` header

**Error: "role is required"**

- Make sure all required fields (role, industry, region) are in the request body

**Error: "Failed to fetch"**

- Backend server might not be running
- Check backend terminal for error messages
- Verify backend URL is correct

## Quick Test Checklist

- [ ] Backend server starts without errors
- [ ] Health endpoint returns `{"status":"ok"}`
- [ ] `/api/analyze` endpoint returns skill data
- [ ] Frontend server starts without errors
- [ ] Frontend homepage loads at `http://localhost:3000`
- [ ] Form submission works
- [ ] Results page displays skills data
- [ ] No CORS errors in browser console
- [ ] Skill cards show percentages
- [ ] Trending skills show arrows (↑ ↓ →)
- [ ] Recommended skills are clearly displayed

## Manual API Testing with Browser

You can also test endpoints directly in the browser:

1. **Open browser Developer Tools (F12)**
2. **Go to Console tab**
3. **Run JavaScript:**

```javascript
// Test analyze endpoint
fetch("http://localhost:5000/api/analyze", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    role: "Backend Engineer",
    industry: "FinTech",
    region: "Global",
  }),
})
  .then((response) => response.json())
  .then((data) => console.log("Success:", data))
  .catch((error) => console.error("Error:", error));
```

If you see the data logged, CORS is working correctly!

## Next Steps

Once everything is working:

1. Try different role/industry combinations
2. Test with different regions
3. Explore the skill visualization (percentages, trends, recommendations)
4. Check browser console for any warnings or errors
5. Test on different browsers (Chrome, Firefox, Edge)

## Need Help?

- Check backend terminal for error messages
- Check frontend terminal for build/compile errors
- Check browser console (F12) for runtime errors
- Verify both servers are running
- Verify environment variables are set correctly
