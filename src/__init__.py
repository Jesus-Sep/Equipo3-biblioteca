"""
M�dulo principal de la API de Gesti�n de Biblioteca Universitaria.
Implementa el patr�n Application Factory para crear instancias de la app.
"""

from flask import Flask, jsonify
from src.config import Config


def create_app(config_class=Config):
    """
    Factory function para crear y configurar una instancia de Flask
    para la API de Biblioteca Universitaria.
    
    Args:
        config_class: Clase de configuraci�n a utilizar
        
    Returns:
        Flask: Instancia de la aplicaci�n configurada
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensiones
    initialize_extensions(app)
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Registrar handlers de errores
    register_error_handlers(app)
    
    # Ruta de salud
    @app.route('/')
    def health_check():
        return jsonify({
            'message': 'API de Gesti�n de Biblioteca Universitaria',
            'status': 'active',
            'version': '1.0'
        })
    
    return app


def initialize_extensions(app):
    """
    Inicializa todas las extensiones de Flask con la aplicaci�n.
    
    Args:
        app: Instancia de Flask
    """
    # Extensiones futuras para base de datos, autenticaci�n, etc.
    pass


def register_blueprints(app):
    """
    Registra todos los blueprints de la aplicaci�n.
    
    Args:
        app: Instancia de Flask
    """
    from src.api.libros import libros_bp
    from src.api.usuarios import usuarios_bp
    from src.api.prestamos import prestamos_bp
    from src.api.autores import autores_bp
    
    app.register_blueprint(libros_bp, url_prefix='/api/libros')
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')
    app.register_blueprint(prestamos_bp, url_prefix='/api/prestamos')
    app.register_blueprint(autores_bp, url_prefix='/api/autores')


def register_error_handlers(app):
    """
    Registra manejadores de errores personalizados para la API.
    
    Args:
        app: Instancia de Flask
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Recurso no encontrado',
            'message': 'El recurso solicitado no existe en la biblioteca'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurri� un error inesperado en el sistema de biblioteca'
        }), 500




