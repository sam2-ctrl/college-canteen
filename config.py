import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Database configuration - SQLite for easy development
    # To use MySQL instead, uncomment the MySQL lines below and comment out SQLite
    # SQLite (NO SETUP REQUIRED - uses local file)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///canteen.db'
    
    # MySQL (Uncomment to use MySQL, update credentials below)
    # DB_USER = os.environ.get('DB_USER') or 'root'
    # DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'password'
    # DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    # DB_PORT = os.environ.get('DB_PORT') or '3306'
    # DB_NAME = os.environ.get('DB_NAME') or 'canteen_db'
    # SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Payment configuration (replace with your actual credentials)
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID') or 'your_razorpay_key_id'
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET') or 'your_razorpay_key_secret'
    
    # File upload configuration
    UPLOAD_FOLDER = 'app/static/images'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
