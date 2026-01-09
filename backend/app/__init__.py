from flask import Flask, jsonify
from flask_cors import CORS
from app.config import config
import os
import logging

# Initialize logger
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config.get(config_name, config['default']))
    
    # Enable CORS (Cross-Origin Resource Sharing) for frontend-backend communication
    # CORS_ORIGINS is a list from config (split from comma-separated string)
    cors_origins_list = app.config.get('CORS_ORIGINS', ['*'])
    
    # Configure CORS based on environment
    # Development: Allow all origins (*) - convenient for local development
    # Production: Restrict to specific frontend domain(s) for security
    if '*' in cors_origins_list:
        # Allow all origins - useful for development and local testing
        # WARNING: In production, ALWAYS set CORS_ORIGINS to specific frontend domain(s)
        # Example: CORS_ORIGINS=http://localhost:3000,https://your-frontend.com
        CORS(app, 
             supports_credentials=False,  # No cookies/credentials needed for this API
             allow_headers=['Content-Type'])
    else:
        # Production mode: Restrict to specific origins for security
        # Only allow requests from specified frontend domains
        # Example: CORS_ORIGINS=https://skill-intelligence.com,https://www.skill-intelligence.com
        CORS(app,
             origins=cors_origins_list,
             supports_credentials=False,
             allow_headers=['Content-Type'])
    
    # Log CORS configuration (safe even if logging not fully configured)
    try:
        if '*' in cors_origins_list:
            logger.info('CORS enabled: allowing all origins (*) - Development mode')
        else:
            logger.info(f'CORS enabled: restricting to origins {cors_origins_list}')
    except Exception:
        pass  # Logging not critical for app startup
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints
    from app.routes.health import health_bp
    app.register_blueprint(health_bp)
    
    # Register API blueprint (for future API routes)
    from app.routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app


def register_error_handlers(app):
    """Register error handlers for JSON responses"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Not Found',
            'message': 'The requested resource was not found.'
        }), 404
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 'Bad Request',
            'message': 'The request was invalid or malformed.'
        }), 400
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': 'An internal server error occurred.'
        }), 500
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 'Method Not Allowed',
            'message': 'The HTTP method is not allowed for this endpoint.'
        }), 405
