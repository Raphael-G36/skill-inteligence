# Skill Intelligence

MVP for Skill Intelligence application.

## Project Structure

```
SI/
├── frontend/          # Next.js frontend application
│   ├── app/          # Next.js App Router
│   ├── public/       # Static assets
│   └── package.json
├── backend/          # Flask REST API
│   ├── app/          # Flask application
│   │   ├── routes/   # API routes
│   │   └── __init__.py
│   └── run.py        # Application entry point
└── README.md
```

## Tech Stack

- **Frontend**: Next.js 14 (App Router), TypeScript, React
- **Backend**: Flask (Python), REST API

## Setup Instructions

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.9+

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file from the example:
   ```bash
   copy .env.example .env
   # or on macOS/Linux:
   cp .env.example .env
   ```

6. Run the Flask development server:
   ```bash
   python run.py
   ```

   The API will be available at [http://localhost:5000](http://localhost:5000)

7. Test the health endpoint:
   ```bash
   curl http://localhost:5000/health
   ```

## Development

### Frontend Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

### Backend Scripts

- `python run.py` - Start Flask development server

## Notes

- Frontend and backend run on separate ports (3000 and 5000)
- **CORS is properly configured** in the Flask backend to allow frontend requests
  - Development: Allows all origins (`CORS_ORIGINS=*`)
  - Production: Restrict to specific frontend domains in `.env`
- Environment variables should be configured in `.env` files (not committed to git)
- CORS is enabled globally and works for all API endpoints and the health check

## Deployment

For production deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md).

**Quick Production Commands:**

Backend:
```bash
gunicorn -c gunicorn.conf.py wsgi:app
```

Frontend:
```bash
npm run build
npm start
```

## Environment Variables

### Backend
- `FLASK_ENV`: Set to `production` for production
- `SECRET_KEY`: Required secret key (generate a strong one)
- `PORT`: Port number (default: 5000)
- `CORS_ORIGINS`: Comma-separated allowed origins

### Frontend
- `NEXT_PUBLIC_API_BASE_URL`: Backend API URL (e.g., `https://api.example.com/api`)

