"""
WSGI entry point for production deployment with Gunicorn
"""
from app import create_app
from dotenv import load_dotenv
import os

load_dotenv()

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    # This should not run in production with Gunicorn
    # Use: gunicorn -c gunicorn.conf.py wsgi:app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

