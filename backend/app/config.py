import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # CORS Configuration
    # Comma-separated list of allowed origins (e.g., "http://localhost:3000,https://example.com")
    # Use '*' for development (allows all origins)
    # In production, specify exact frontend domain(s)
    cors_origins_env = os.environ.get('CORS_ORIGINS', '*')
    CORS_ORIGINS = [origin.strip() for origin in cors_origins_env.split(',') if origin.strip()]
    
    # API Configuration
    API_TIMEOUT = int(os.environ.get('API_TIMEOUT', 30))


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

