"""
Blueprint para gestión de autores de la biblioteca.
Maneja información sobre los autores de los libros.
"""

from flask import Blueprint, jsonify, request

autores_bp = Blueprint('autores', __name__)

# Datos de ejemplo
autores = [
    {
        'id': 1,
        'nombre': 'Gabriel García Márquez',
        'nacionalidad': 'Colombiana',
        'fecha_nacimiento': '1927-03-06',
        'biografia': 'Premio Nobel de Literatura 1982...',
        'libros_ids': [1]
    },
    {
        'id': 2,
        'nombre': 'Miguel de Cervantes',
        'nacionalidad': 'Española',
        'fecha_nacimiento': '1547-09-29',
        'biografia': 'Autor de El Quijote...',
        'libros_ids': [2]
    }
]


@autores_bp.route('/', methods=['GET'])
def obtener_autores():
    """
    Obtiene todos los autores del catálogo.
    
    Returns:
        JSON: Lista de autores
    """
    return jsonify({
        'autores': autores,
        'total': len(autores)
    })


@autores_bp.route('/<int:autor_id>', methods=['GET'])
def obtener_autor(autor_id):
    """
    Obtiene un autor específico por su ID.
    
    Args:
        autor_id: ID del autor
        
    Returns:
        JSON: Datos del autor
    """
    autor = next((a for a in autores if a['id'] == autor_id), None)
    
    if autor is None:
        return jsonify({'error': 'Autor no encontrado'}), 404
    
    return jsonify({'autor': autor})