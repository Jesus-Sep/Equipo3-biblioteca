import os
from datetime import timedelta

class BaseConfig:
    """Configuraci�n base para todos los entornos"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    """Configuraci�n para desarrollo"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'sqlite:///biblioteca_development.db'
    )

class TestingConfig(BaseConfig):
    """Configuraci�n para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///biblioteca_testing.db'

class ProductionConfig(BaseConfig):
    """Configuraci�n para producci�n"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

