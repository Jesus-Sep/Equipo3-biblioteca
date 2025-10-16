"""
Paquete API para la Biblioteca Universitaria

Este paquete contiene todos los blueprints y endpoints de la API REST.
"""

from src.api.biblioteca import biblioteca_bp

# Exportar todos los blueprints para fácil acceso
__all__ = ['biblioteca_bp']

# Versión del paquete API
__version__ = '1.0.0'