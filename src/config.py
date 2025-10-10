"""
Configuración centralizada para la API de Biblioteca Universitaria.
Permite diferentes configuraciones por entorno.
"""

import os
from datetime import timedelta


class Config:
    """Configuración base para todos los entornos."""
    
    # Clave secreta para sesiones y seguridad
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'biblioteca-universitaria-secret-key'
    
    # Configuración de Flask
    DEBUG = False
    TESTING = False
    JSON_SORT_KEYS = False
    
    # Configuración de la API
    API_TITLE = 'API de Gestión de Biblioteca Universitaria'
    API_VERSION = '1.0'
    API_DESCRIPTION = 'Sistema de gestión para biblioteca universitaria'
    
    # Límites de la biblioteca
    MAX_LIBROS_PRESTAMO = 5
    DIAS_PRESTAMO = 15
    MULTA_POR_DIA = 2.50
    
    # Configuración de base de datos (futura implementación)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///biblioteca.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración JWT (futura implementación)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-biblioteca-secret'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)


class DevelopmentConfig(Config):
    """Configuración para entorno de desarrollo."""
    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///biblioteca_dev.db'


class TestingConfig(Config):
    """Configuración para entorno de testing."""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'testing-biblioteca-secret-key'
    MAX_LIBROS_PRESTAMO = 3  # Para testing


class ProductionConfig(Config):
    """Configuración para entorno de producción."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY debe estar configurada en producción")


# Mapeo de configuraciones por entorno
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}