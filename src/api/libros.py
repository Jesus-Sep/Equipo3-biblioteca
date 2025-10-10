"""
Blueprint para gestión de libros en la biblioteca universitaria.
Maneja todas las operaciones relacionadas con el catálogo de libros.
"""

from flask import Blueprint, jsonify, request

libros_bp = Blueprint('libros', __name__)

# Datos de ejemplo (reemplazar con base de datos)
libros = [
    {
        'id': 1,
        'titulo': 'Cien años de soledad',
        'autor': 'Gabriel García Márquez',
        'isbn': '978-8437604947',
        'categoria': 'Novela',
        'ejemplares_disponibles': 5,
        'ejemplares_totales': 8
    },
    {
        'id': 2,
        'titulo': 'El Quijote de la Mancha',
        'autor': 'Miguel de Cervantes',
        'isbn': '978-8467031250',
        'categoria': 'Clásico',
        'ejemplares_disponibles': 3,
        'ejemplares_totales': 5
    }
]


@libros_bp.route('/', methods=['GET'])
def obtener_libros():
    """
    Obtiene todos los libros del catálogo.
    
    Returns:
        JSON: Lista de todos los libros disponibles
    """
    return jsonify({
        'libros': libros,
        'total': len(libros)
    })


@libros_bp.route('/<int:libro_id>', methods=['GET'])
def obtener_libro(libro_id):
    """
    Obtiene un libro específico por su ID.
    
    Args:
        libro_id: ID del libro a buscar
        
    Returns:
        JSON: Datos del libro o error 404
    """
    libro = next((l for l in libros if l['id'] == libro_id), None)
    
    if libro is None:
        return jsonify({'error': 'Libro no encontrado'}), 404
    
    return jsonify({'libro': libro})


@libros_bp.route('/', methods=['POST'])
def crear_libro():
    """
    Crea un nuevo libro en el catálogo.
    
    Returns:
        JSON: Datos del libro creado
    """
    data = request.get_json()
    
    if not data or not all(key in data for key in ['titulo', 'autor', 'isbn']):
        return jsonify({'error': 'Datos incompletos'}), 400
    
    nuevo_libro = {
        'id': len(libros) + 1,
        'titulo': data['titulo'],
        'autor': data['autor'],
        'isbn': data['isbn'],
        'categoria': data.get('categoria', 'General'),
        'ejemplares_disponibles': data.get('ejemplares_disponibles', 1),
        'ejemplares_totales': data.get('ejemplares_totales', 1)
    }
    
    libros.append(nuevo_libro)
    
    return jsonify({
        'message': 'Libro creado exitosamente',
        'libro': nuevo_libro
    }), 201


@libros_bp.route('/buscar', methods=['GET'])
def buscar_libros():
    """
    Busca libros por título, autor o categoría.
    
    Query Params:
        q: Término de búsqueda
        tipo: 'titulo', 'autor' o 'categoria'
        
    Returns:
        JSON: Libros que coinciden con la búsqueda
    """
    query = request.args.get('q', '').lower()
    tipo = request.args.get('tipo', 'titulo')
    
    if not query:
        return jsonify({'error': 'Término de búsqueda requerido'}), 400
    
    resultados = []
    
    for libro in libros:
        if tipo == 'titulo' and query in libro['titulo'].lower():
            resultados.append(libro)
        elif tipo == 'autor' and query in libro['autor'].lower():
            resultados.append(libro)
        elif tipo == 'categoria' and query in libro.get('categoria', '').lower():
            resultados.append(libro)
    
    return jsonify({
        'resultados': resultados,
        'total': len(resultados),
        'query': query,
        'tipo': tipo
    })